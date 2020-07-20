import pytest
from ua_gen import consts as c
from ua_gen import cli
import json
import gzip
import os


@pytest.fixture
def ua_defs_file():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "20200716-user-agents.json.gz")
    with gzip.GzipFile(file_path, 'r') as f:
        return json.loads(f.read().decode('utf-8'))


def test_chrome_desktop(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        ua = uagen.get_ua(["chrome", "desktop"])
        assert("Chrome" in ua)
        assert("Firefox" not in ua)


def test_mobile_select(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["mobile"])
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == "mobile")


def test_mobile_chrome(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["mobile", "chrome"])
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == "mobile")


def test_desktop_linux_opera(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["desktop", "linux", "opera"])
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == "desktop")
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Opera")
        assert("Linux" in uagen.selected_ua[c.UA_USERAGENT])


def test_firefox_desktop(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["firefox", "desktop"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Firefox")
        assert("Firefox" in uagen.selected_ua[c.UA_USERAGENT])


def test_firefox_mobile(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["firefox", "mobile"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Firefox")
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == "mobile")
        assert("FxiOS" in uagen.selected_ua[c.UA_USERAGENT])


def test_ie(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["ie"])
        assert("MSIE" in uagen.selected_ua[c.UA_USERAGENT] or
               "Trident" in uagen.selected_ua[c.UA_USERAGENT])


def test_edge(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["edge"])
        assert("Edg/" in uagen.selected_ua[c.UA_USERAGENT] or
               "EdgA/" in uagen.selected_ua[c.UA_USERAGENT])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Edge")


def test_edge_desktop(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["edge", "desktop"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Edge")
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == "desktop")


def test_edge_mobile(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["edge", "mobile"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Edge")
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == "mobile")


def test_safari(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["safari"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == 'Safari')
        assert("AppleWebKit" in uagen.selected_ua[c.UA_USERAGENT])


def test_facebook(ua_defs_file):
    uagen = cli.UAGen(ua_defs_file)

    for _ in range(1, 100):
        uagen.get_ua(["fb"])
        assert("Facebook" in uagen.selected_ua[c.UA_USERAGENT] or
               "FBAV" in uagen.selected_ua[c.UA_USERAGENT] or
               "FBAN" in uagen.selected_ua[c.UA_USERAGENT] or
               "FB_IAB" in uagen.selected_ua[c.UA_USERAGENT])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == 'Facebook')


def test_qq_desktop(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["qq", "desktop"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == 'QQ Browser')
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == 'desktop')


def test_qq_mobile(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["qq", "mobile"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == 'QQ Browser')
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == 'mobile')


def test_uc_desktop(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["uc", "desktop"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == 'UC Browser')
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == 'desktop')


def test_uc_mobile(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["uc", "mobile"])
        assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == 'UC Browser')
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == 'mobile')


## OS

def test_win(ua_defs_file):
    uagen = cli.UAGen(ua_defs_file)
    
    for _ in range(1, 100):
        uagen.get_ua(["win"])
        assert(uagen.selected_ua[c.UA_PLATFORM] == 'Windows')


def test_win_alias(ua_defs_file):
    uagen = cli.UAGen(ua_defs_file)

    for _ in range(1, 100):
        uagen.get_ua(["windows"])
        assert(uagen.selected_ua[c.UA_PLATFORM] == 'Windows')


def test_win_alias2(ua_defs_file):
    uagen = cli.UAGen(ua_defs_file)

    for _ in range(1, 100):
        uagen.get_ua(["win32"])
        assert(uagen.selected_ua[c.UA_PLATFORM] == 'Windows')


def test_ios(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["ios"])
        assert(uagen.selected_ua[c.UA_PLATFORM] == 'iOS')


def test_android(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["android"])
        assert(uagen.selected_ua[c.UA_PLATFORM] == 'Android')


## filter errors


def test_no_matches(ua_defs_file):
    uagen = cli.UAGen(ua_defs_file)
    try:
        uagen.get_ua(["sadafdhfd"])
        assert(False)
    except cli.NoUserAgentFoundException:
        pass


def test_not_recognised_alias(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["trident"])
        assert("Trident" in uagen.selected_ua[c.UA_USERAGENT])


def test_not_recognised_alias_plus_filter(ua_defs_file):
    for _ in range(1, 100):
        uagen = cli.UAGen(ua_defs_file)
        uagen.get_ua(["nokia", "mobile"])
        assert("Nokia" in uagen.selected_ua[c.UA_USERAGENT])
        assert(uagen.selected_ua[c.UA_DEVICE_CATEGORY] == "mobile")


@pytest.mark.warnings
def test_warn_on_conflicting_platform(ua_defs_file, caplog):
    uagen = cli.UAGen(ua_defs_file)
    uagen.get_ua(["safari", "firefox"])
    # captured = caplog.text
    assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Safari")
    assert("* You already have a browser family (Safari) set and you tried to set another, so I'm ignoring 'firefox'"
           in caplog.text)


@pytest.mark.warnings
def test_warn_on_conflicting_platform_reverse(caplog, ua_defs_file):
    from sys import stderr
    uagen = cli.UAGen(ua_defs_file)
    uagen.get_ua(["firefox", "safari"])
    assert(uagen.selected_ua[c.UA_BROWSER_FAMILY] == "Firefox")
    assert("* You already have a browser family (Firefox) set and you tried to set another, so I'm ignoring 'safari'"
           in caplog.text)
