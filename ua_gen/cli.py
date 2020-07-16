"""uagen

Usage:
  uagen
  uagen <match> <match>
  uagen --update-db
  uagen (-h | --help)
  uagen --version

Options:
  uagen        Return any random UA, weighted by usage.
  uagen <match> <match>
              Give a number of keyword criteria like 'Win', 'Firefox'
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

UA_DB_URL = 'https://raw.githubusercontent.com/intoli/user-agents/master/src/user-agents.json.gz'
UA_DB_STALE_SECONDS = 24 * 60 * 60 * 30


def main():
    """Generates random but realistic user agents on a command line (or via API)"""
    args = docopt(__doc__)

    if (args["--update-db"]):
        ua_db = UADBManager()
        ua_db.fetch_db()

    uagen = UAGen()
    print(uagen.get_ua(args))


class UAGen(object):
    def __init__(self):
        self.db_manager = UADBManager()
        if (self.db_manager.is_too_old()):
            logger.info("UA DB stale, fetching a fresh one...")
            self.db_manager.fetch_db()

        self.ua_db = self.db_manager.get_ua_defs()

    def get_filters(self):
        pass

    def get_ua(self, os=None, browser=None, regex=None):
        self.ua_db = None


class UADBManager(object):
    def __init__(self):
        self.db_dir = os.path.join(os.path.expanduser("~"), ".ua-gen-cli/")
        self.db_file = os.path.join(self.db_dir, "ua_db.json")

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        logger.debug(f"DB file: {self.db_file}")

        self.load_filtered_ua_defs()

    def fetch_db(self):
        r = requests.get(UA_DB_URL, stream=True)

        if r.ok:
            with open(self.db_file, "wb") as f:
                r.raw.decode_content = True
                gzip_file = gzip.GzipFile(fileobj=r.raw)
                shutil.copyfileobj(gzip_file, f)

    def is_too_old(self):
        stat = os.stat(self.db_file)
        epoch_now = int(time.time())

        return((epoch_now - stat.st_mtime) > UA_DB_STALE_SECONDS)

    def load_filtered_ua_defs(self):
        for entry in json.load(self.db_file):
            self.ua_db.append({
                'appName': entry.get("appName"),
                'platform': entry.get("platform"),
                'userAgent': entry.get("userAgent"),
                'deviceCategory': entry.get("deviceCategory"),
                'weight': entry.get("weight")
            })


if __name__ == "__main__":
    main()
