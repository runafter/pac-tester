import sys
import urllib2
import re

def commented(s):
    return s.startswith("#")


class Matcher:
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return self.rule

    def match(self, response):
        return False


class ResponseCodeMatcher(Matcher):
    def __init__(self, regex):
        self.regex = regex

    def match(self, response):
        return re.match(self.regex, str(response.getcode()))


class Matchers:
    matchers = {
        "CODE": ResponseCodeMatcher
    }

    @staticmethod
    def of(rule):
        rule = str(rule)
        i = rule.index(":")
        method = rule[:i]
        args = rule[(i+1):]
        return Matchers.matchers[method](args)


class PacTestCase:
    def __init__(self, raw):
        self.raw = raw
        parsed = str(raw).split(",")
        self.url = parsed[0]
        self.expected = Matchers.of(parsed[1])

    def __str__(self):
        return " ".join((self.url, str(self.expected)))

    def proxy_handler(self):
        # return urllib2.BaseHandler()\
        return urllib2.ProxyHandler({"http": "http://210.101.131.231:8080"})
        #return urllib2.ProxyHandler({"http": "http://106.249.176.213:80"})
        #return urllib2.ProxyHandler({"https": "http://210.96.153.20:3128"})

    def check(self):
        req = urllib2.Request(self.url)
        print("HOST " + req.get_host())
        opener = urllib2.build_opener(self.proxy_handler())
        res = opener.open(req)
        code = res.getcode()
        headers = res.info().headers
        #body = res.read()
        print("RESPONSE", code, headers)
        succ = self.expected.match(res)

        return " ".join(("SUCC", "")) if succ else "FAIL"


#while True:
    # line = sys.stdin.readline().strip()
    # if not line or len(line) == 0:
    #     break
    # if commented(line):
    #     continue
    # print(str(PacTestCase(line).check()))

print(str(PacTestCase("http://google.com,CODE:200").check()))
print(str(PacTestCase("https://google.com,CODE:200").check()))
