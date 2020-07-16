rules = {
    'mobile': {'aliases': ['mob'], 'cat': 'deviceCategory'},
    'desktop': {'aliases': ['desk'], 'cat': 'deviceCategory'},
    'tablet': {'aliases': ['tab'], 'cat': 'deviceCategory'},
    'Netscape': {'aliases': ['Firefox', 'firefox', 'ff'], 'regex': 'Firefox/\\d'},
    'MSIE': {'aliases': ['ie', 'IE', 'msie'], 'regex': 'MSIE \\d'},
    'Opera': {'aliases': ['opera'], 'cat': 'appName'},
    # Chrome, which we have to define more specifically since everyone has in agent
    'Google Inc.': {'aliases': ['Chrome', 'chrome'], 'cat': 'vendor', 'regex': 'Chrome'},
    'Win32': {'aliases': ['win', 'Win', 'windows'], 'cat': 'platform'},
    'MacIntel': {'aliases': ['osx', 'Mac', 'MacOS'], 'cat': 'platform'},
    'Linux x86_64': {'aliases': ['linux'], 'cat': 'platform'},
}