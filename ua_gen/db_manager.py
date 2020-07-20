import os
import requests
import gzip
import shutil
import json
import time

from user_agents import parse as ua_parse

from .logging import logger
from . import consts as c


class UADBManager(object):
    """
    Manages downloading, enriching, updating, and returning the master list
    of user agent definitions.

    The original UA definitions file has some inaccuracies, notably listing
    the vendor as Google everywhere, including for IE. Since it has valuable
    weightings as seen in a user population, we instead do some of our own
    user agent parsing with user_agents for higher accuracy.
    """
    def __init__(self, force_db_update=False):
        self.db_dir = os.path.join(os.path.expanduser("~"), ".ua-gen-cli/")
        self.raw_db_file_path = os.path.join(self.db_dir, "raw_ua_db.json")
        self.db_file_path = os.path.join(self.db_dir, "enriched_ua_db.json")

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        logger.debug(f"DB file: {self.db_file_path}")
        if (force_db_update or self.no_db_file_present or self.is_too_old):
            self.fetch_db()

        self.ua_db = []

    def fetch_db(self):
        logger.error("Fetching and enriching user agent DB - we'll be much faster on the next run, scout's honour!")

        r = requests.get(c.UA_DB_URL, stream=True)

        if r.ok:
            with open(self.raw_db_file_path, "wb") as f:
                r.raw.decode_content = True
                gzip_file = gzip.GzipFile(fileobj=r.raw)
                shutil.copyfileobj(gzip_file, f)

        self.enrich_db()

    def enrich_db(self):
        # the DB file we get is very useful, but inaccurate in places
        # for OS and the like.
        # We enrich using a UA parsing lib for better consistency.

        wf = open(self.db_file_path, 'w')

        entries = []

        with open(self.raw_db_file_path) as rf:
            for entry in json.load(rf):
                parsed_ua = ua_parse(entry.get(c.UA_USERAGENT))
                entry = self.update_ua_db_entry(entry, parsed_ua)
                entries.append(entry)

            wf.write(json.dumps(entries))

        wf.close()

    def update_ua_db_entry(self, entry, parsed_ua):
        entry[c.UA_BROWSER_FAMILY] = parsed_ua.browser.family
        entry[c.UA_PLATFORM] = parsed_ua.os.family
        entry[c.UA_DEVICE_CATEGORY] = self._get_device_category(parsed_ua)

        # we need a more granular setting, so we split some compound family labels up
        if entry[c.UA_BROWSER_FAMILY] == "Chrome Mobile":
            entry[c.UA_BROWSER_FAMILY] = "Chrome"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
        if entry[c.UA_BROWSER_FAMILY] == "Chrome Mobile iOS":
            entry[c.UA_BROWSER_FAMILY] = "Chrome"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
            entry[c.UA_PLATFORM] = "iOS"
        if entry[c.UA_BROWSER_FAMILY] == "Chrome Mobile WebView":
            entry[c.UA_BROWSER_FAMILY] = "Chrome"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
        if entry[c.UA_BROWSER_FAMILY] == "Edge Mobile":
            entry[c.UA_BROWSER_FAMILY] = "Edge"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
        elif entry[c.UA_BROWSER_FAMILY] == "Mobile Safari":
            entry[c.UA_BROWSER_FAMILY] = "Safari"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
        elif entry[c.UA_BROWSER_FAMILY] == "QQ Browser Mobile":
            entry[c.UA_BROWSER_FAMILY] = "QQ Browser"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
        elif entry[c.UA_BROWSER_FAMILY] == "UC Browser Mobile":
            entry[c.UA_BROWSER_FAMILY] = "UC Browser"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
        elif entry[c.UA_BROWSER_FAMILY] == "Firefox iOS":
            entry[c.UA_BROWSER_FAMILY] = "Firefox"
            entry[c.UA_DEVICE_CATEGORY] = "mobile"
            entry[c.UA_PLATFORM] = "iOS"

        return entry

    @property
    def is_too_old(self):
        try:
            stat = os.stat(self.db_file_path)
        except FileNotFoundError:
            return True   # actually doesn't exist, but that's too old for our purposes
        epoch_now = int(time.time())

        return((epoch_now - stat.st_mtime) > c.UA_DB_STALE_SECONDS)

    @property
    def no_db_file_present(self):
        return not os.path.isfile(self.db_file_path)

    def load_ua_defs(self):
        with open(self.db_file_path) as f:
            for entry in json.load(f):
                self.ua_db.append(entry)
        return(self.ua_db)

    def _get_device_category(self, parsed_ua):
        if parsed_ua.is_mobile:
            return 'mobile'
        elif parsed_ua.is_pc:
            return 'desktop'
        elif parsed_ua.is_tablet:
            return 'tablet'
        elif parsed_ua.is_bot:
            return 'bot'

