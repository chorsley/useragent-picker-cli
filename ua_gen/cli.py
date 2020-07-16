"""uagen

Usage:
  uagen
  uagen <match> <match>
  uagen --update-cache
  uagen (-h | --help)
  uagen --version

Options:
  uagen       Return any random UA, weighted by usage.
  uagen <match> <match>
              Give a number of keyword criteria like 'Win', 'Firefox'
  -h --help   Show this screen.
  --version   Show version.
"""

import os.path
import shutil
import gzip
from os.path import expanduser

from docopt import docopt
import requests

UA_DB_URL = 'https://raw.githubusercontent.com/intoli/user-agents/master/src/user-agents.json.gz'


def main():
    """Generates random but realistic user agents on a command line (or via API)"""
    args = docopt(__doc__)

    uagen = UAGen()
    print(uagen.get_ua(args))


class UAGen(object):
    def __init__(self):
        self.db_manager = UADBManager()
        if (self.db_manager.is_too_old):
            self.db_manager.fetch_db()

        self.ua_db = self.db_manager.get_ua_defs()

    def get_filters(self):
        pass

    def get_ua(self, os=None, browser=None, regex=None):
        self.ua_db = None


class UADBManager(object):
    def __init__(self):
        self.db_dir = os.path.join(expanduser("~"), ".ua-gen-cli/")
        self.db_file = os.path.join(self.db_dir, "ua_db.json")

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        print(self.db_file)

    def fetch_db(self):
        r = requests.get(UA_DB_URL, stream=True)

        if r.ok:
            with open(self.db_file, "wb") as f:
                r.raw.decode_content = True
                gzip_file = gzip.GzipFile(fileobj=r.raw)
                shutil.copyfileobj(gzip_file, f)

    def is_too_old(self):
        pass

    def get_ua_defs(self):
        pass


if __name__ == "__main__":
    main()
