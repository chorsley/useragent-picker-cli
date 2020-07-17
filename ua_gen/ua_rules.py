ua_rules = [
    {'match': 'mobile', 'aliases': ['mob'], 'cat': 'deviceCategory'},
    {'match': 'desktop', 'aliases': ['desk'], 'cat': 'deviceCategory'},
    {'match': 'tablet', 'aliases': ['tab'], 'cat': 'deviceCategory'},
    {'match': 'Netscape', 'aliases': ['firefox', 'ff'], 'regex': 'Firefox/\\d', 'cat': 'vendor'},
    {'match': 'MSIE', 'aliases': ['ie', 'msie'], 'regex': 'MSIE \\d', 'cat': 'vendor'},
    {'match': 'Opera', 'aliases': ['opera'], 'cat': 'appName'},
    # Chrome, which we have to define more specifically since everyone has in agent
    {'match': 'Google Inc.', 'aliases': ['chrome'], 'cat': 'vendor', 'regex': 'Chrome'},
    {'match': 'Win32', 'aliases': ['win', 'windows'], 'cat': 'platform'},
    {'match': 'MacIntel', 'aliases': ['osx', 'Mac', 'MacOS'], 'cat': 'platform'},
    {'match': 'Linux x86_64', 'aliases': ['linux'], 'cat': 'platform'},
]

__all__ = ['ua_rules']