ua_rules = [
    # match is an exact field match on the 'cat' field listed.
    # regex is applied on the userAgent field.
    # aliases are anything the user might reasonably enter to trigger the match.
    # aliases must be unique across all entries, or some matches will get skipped.
    # aliases should be lowercase for consistency
    {'match': 'mobile', 'aliases': ['mobile', 'mob'], 'cat': 'deviceCategory'},
    {'match': 'desktop', 'aliases': ['desktop', 'desk'], 'cat': 'deviceCategory'},
    {'match': 'tablet', 'aliases': ['tablet', 'tab'], 'cat': 'deviceCategory'},
    {'match': 'Firefox', 'aliases': ['netscape', 'firefox', 'ff'], 'cat': 'browser_family'},
    {'match': 'IE', 'aliases': ['ie', 'msie', 'iexplore', 'internet explorer'], 'cat': 'browser_family'},
    {'match': 'Edge', 'aliases': ['edge'], 'cat': 'browser_family'},
    {'match': 'Opera', 'aliases': ['opera'], 'cat': 'browser_family'},
    {'match': 'Safari', 'aliases': ['safari'], 'cat': 'browser_family'},
    # Chrome, which we have to define more specifically since everyone has in agent
    {'match': 'Chrome', 'aliases': ['chrome'], 'cat': 'browser_family'},
    {'match': 'Windows', 'aliases': ['win32', 'win', 'windows'], 'cat': 'platform'},
    {'match': 'Mac OS X', 'aliases': ['macintel', 'osx', 'Mac', 'MacOS'], 'cat': 'platform'},
    {'match': 'Linux', 'aliases': ['linux', 'x11'], 'cat': 'platform'},
]

__all__ = ['ua_rules']