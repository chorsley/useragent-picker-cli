from . import consts as c

ua_rules = [
    # match is an exact field match on the 'cat' field listed.
    # regex is applied on the userAgent field.
    # aliases are anything the user might reasonably enter to trigger the match.
    # aliases must be unique across all entries, or some matches will get skipped.
    # aliases should be lowercase for consistency
    {'match': 'mobile', 'aliases': ['mobile', 'mob'], 'cat': c.UA_DEVICE_CATEGORY},
    {'match': 'desktop', 'aliases': ['desktop', 'desk'], 'cat': c.UA_DEVICE_CATEGORY},
    {'match': 'tablet', 'aliases': ['tablet', 'tab'], 'cat': c.UA_DEVICE_CATEGORY},

    {'match': 'Firefox', 'aliases': ['netscape', 'firefox', 'ff'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'IE', 'aliases': ['ie', 'msie', 'iexplore', 'internet explorer'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'Edge', 'aliases': ['edge'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'Opera', 'aliases': ['opera'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'Safari', 'aliases': ['safari'], 'cat': c.UA_BROWSER_FAMILY},
    # Chrome, which we have to define more specifically since everyone has in agent
    {'match': 'Chrome', 'aliases': ['chrome'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'Chromium', 'aliases': ['chromium'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'Facebook', 'aliases': ['facebook', 'fb'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'UC Browser', 'aliases': ['uc', 'ucbrowser'], 'cat': c.UA_BROWSER_FAMILY},
    {'match': 'QQ Browser', 'aliases': ['qq', 'qqbrowser'], 'cat': c.UA_BROWSER_FAMILY},

    {'match': 'Windows', 'aliases': ['win32', 'win', 'windows'], 'cat': c.UA_PLATFORM},
    {'match': 'Mac OS X', 'aliases': ['macintel', 'osx', 'Mac', 'MacOS'], 'cat': c.UA_PLATFORM},
    {'match': 'Linux', 'aliases': ['linux', 'x11'], 'cat': c.UA_PLATFORM},
    {'match': 'iOS', 'aliases': ['ios', 'iphone'], 'cat': c.UA_PLATFORM},
    {'match': 'Android', 'aliases': ['android'], 'cat': c.UA_PLATFORM},
]

__all__ = ['ua_rules']