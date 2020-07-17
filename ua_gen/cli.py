"""uagen

Usage:
  uagen
  uagen [--update-db] FILTER...
  uagen (-h | --help)
  uagen --version

Arguments:
  FILTER...
              Give a number of keyword filters like 'Win', 'Firefox'

Options:
  --update-db  Force an update of the UA DB cache
  -h --help    Show this screen.
  --version    Show version.
"""

import os.path
import shutil
import gzip
import os
import time
import json

from docopt import docopt
import requests
from loguru import logger

from ua_gen import ua_rules

UA_DB_URL = 'https://raw.githubusercontent.com/intoli/user-agents/master/src/user-agents.json.gz'
UA_DB_STALE_SECONDS = 24 * 60 * 60 * 30


def main():
    """Generates random but realistic user agents on a command line (or via API)"""
    args = docopt(__doc__)

    if (args["--update-db"]):
        ua_db = UADBManager()
        ua_db.fetch_db()

    uagen = UAGen()
    print(uagen.get_ua(aliases=args["FILTER"]))


class UAGen(object):
    def __init__(self):
        self.db_manager = UADBManager()
        if (self.db_manager.is_too_old()):
            logger.info("UA DB stale, fetching a fresh one...")
            self.db_manager.fetch_db()

        self.ua_db = self.db_manager.load_ua_defs()
        self.filtered_ua_db = []
        self.ua_rule = None

    def get_ua(self, aliases):
        self.ua_rule = UARuleManager(aliases)

        self.ua_rule.build_rules()
        self.filter_uas()

    def filter_uas(self):
        for ua_entry in self.ua_db:
            for criteria in ['platform', 'vendor', 'deviceCategory']:
                if getattr(self.ua_rule, criteria) and ua_entry.get(criteria) == getattr(self.ua_rule, criteria):
                    pass
            else:
                continue
            self.filtered_ua_db.append(ua_entry)
        print(self.filtered_ua_db)


class UARuleManager(object):
    def __init__(self, aliases=None, strmatch=None):
        self.aliases = [] if None else aliases
        self.strmatch = strmatch
        self.platform = None
        self.vendor = None
        self.deviceCategory = None

    def build_rules(self):
        for rule in ua_rules:
            for alias in map(lambda x: x.lower(), self.aliases):
                if alias in map(lambda y: y.lower(), rule["aliases"]):
                    self.set_rule(alias, rule)

    def set_rule(self, alias, rule):
        if not self.vendor and rule.cat['vendor']:
            self.vendor = rule['match']
        elif rule.cat['vendor']:
            logger.warn("You already have a browser vendor f{self.vendor} set and you tried to set"
                        "another, but I'm ignoring it: f{alias}")
        
        if not self.platform and rule.cat['platform']:
            self.platform = rule['match']
        elif rule.cat['platform']:
            logger.warn("You already have an OS f{self.playform} set and you tried to set"
                        "another, but I'm ignoring it: f{alias}")

        if not self.device and rule.cat['deviceCategory']:
            self.deviceCategory = rule['deviceCategory']
        elif rule.cat['deviceCategory']:
            logger.warn("You already have an OS f{self.playform} set and you tried to set")


class UADBManager(object):
    def __init__(self):
        self.db_dir = os.path.join(os.path.expanduser("~"), ".ua-gen-cli/")
        self.db_file_path = os.path.join(self.db_dir, "ua_db.json")

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        logger.debug(f"DB file: {self.db_file_path}")

        self.ua_db = []
        self.load_ua_defs()

    def fetch_db(self):
        r = requests.get(UA_DB_URL, stream=True)

        if r.ok:
            with open(self.db_file_path, "wb") as f:
                r.raw.decode_content = True
                gzip_file = gzip.GzipFile(fileobj=r.raw)
                shutil.copyfileobj(gzip_file, f)

    def is_too_old(self):
        stat = os.stat(self.db_file_path)
        epoch_now = int(time.time())

        return((epoch_now - stat.st_mtime) > UA_DB_STALE_SECONDS)

    def load_ua_defs(self):
        with open(self.db_file_path) as f:
            for entry in json.load(f):
                self.ua_db.append({
                    'appName': entry.get("appName"),
                    'platform': entry.get("platform"),
                    'userAgent': entry.get("userAgent"),
                    'deviceCategory': entry.get("deviceCategory"),
                    'weight': entry.get("weight")
                })
        return(self.ua_db)


if __name__ == "__main__":
    main()
