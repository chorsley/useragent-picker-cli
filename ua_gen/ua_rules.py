ua_rules = [
    # match is an exact field match on the 'cat' field listed.
    # regex is applied on the userAgent field.
    # aliases are anything the user might reasonably enter to trigger the match.
    # aliases must be unique across all entries, or some matches will get skipped.
    # aliases should be lowercase for consistency
    {'match': 'mobile', 'aliases': ['mobile', 'mob'], 'cat': 'deviceCategory'},
    {'match': 'desktop', 'aliases': ['desktop', 'desk'], 'cat': 'deviceCategory'},
    {'match': 'tablet', 'aliases': ['tablet', 'tab'], 'cat': 'deviceCategory'},
    {'match': 'Netscape', 'aliases': ['netscape', 'firefox', 'ff'], 'regex': r'Firefox/\d', 'cat': 'appName'},
    # TODO: bad detection in file here
    {'match': 'Google Inc.', 'aliases': ['ie', 'msie'], 'regex': r'MSIE \d', 'cat': 'vendor'},
    # TODO: match is way too broad, but regex saves it.
    # TODO: seems to be a detection issue in file, should switch to own UA feature detection
    {'match': 'Win32', 'aliases': ['edge'], 'cat': 'platform', 'regex': r'Edg/\d'},
    # TODO: missing from DB currently?
    # {'match': 'Opera', 'aliases': ['opera'], 'cat': 'appName'},
    # Chrome, which we have to define more specifically since everyone has in agent
    {'match': 'Google Inc.', 'aliases': ['chrome'], 'cat': 'vendor', 'regex': r'Chrome'},
    {'match': 'Win32', 'aliases': ['win32', 'win', 'windows'], 'cat': 'platform'},
    {'match': 'MacIntel', 'aliases': ['macintel', 'osx', 'Mac', 'MacOS'], 'cat': 'platform'},
    {'match': 'Linux x86_64', 'aliases': ['linux', 'x11'], 'cat': 'platform'},
    # TODO: not much to separate it from Chrome unless you have good detection, so we need to add this.
    {'match': 'Netscape', 'aliases': ['safari'], 'cat': 'appName', 'regex': r'AppleWebKit/\d'},
]

__all__ = ['ua_rules']