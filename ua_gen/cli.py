"""uagen

Usage:
  uagen
  uagen [--force-update-db] FILTER...
  uagen (-h | --help)
  uagen --version

Arguments:
  FILTER...
              Give a number of keyword filters like 'Win', 'Firefox'

Options:
  --force-update-db  Force an update of the UA DB cache
  -h --help          Show this screen.
  --version          Show version.
"""

import os.path
import shutil
import gzip
import os
import time
import json
import random
import re
import sys

from docopt import docopt
import requests
from loguru import logger

from user_agents import parse as ua_parse

from ua_gen import ua_rules

UA_DB_URL = 'https://raw.githubusercontent.com/intoli/user-agents/master/src/user-agents.json.gz'
UA_DB_STALE_SECONDS = 24 * 60 * 60 * 30

logger.remove()
logger.add(sys.stderr, format="{message}", level="INFO")


class NoUserAgentFoundException(Exception):
    pass


def main(args):
    """Generates random but realistic user agents on a command line (or via API)"""
    if (args["--force-update-db"]):
        ua_db = UADBManager()
        ua_db.fetch_db()

    uagen = UAGen()

    try:
        print(uagen.get_ua(aliases=args["FILTER"]))
    except NoUserAgentFoundException:
        logger.error("Sorry, I couldn't find any user agents matching your criteria.\n")
        logger.error("Remember, the UA list contains agents seen in the wild, so if you want something very exotic, ")
        logger.error("you might need to go and find it elsewhere.") 
        sys.exit(1)


class UAGen(object):
    def __init__(self, ua_db=None):
        # normal operation
        if not ua_db:
            self.db_manager = UADBManager()
            if (self.db_manager.is_too_old()):
                logger.info("UA DB stale, fetching a fresh one...")
                self.db_manager.fetch_db()

            self.ua_db = self.db_manager.load_ua_defs()
        # usually for testing
        else:
            self.ua_db = ua_db
        self.filtered_ua_db = []
        self.ua_rule = None
        self.selected_ua = None

    def get_ua(self, aliases: list) -> None:
        self.filtered_ua_db = []  # reset for each run of get_ua()
        self.ua_rule = UARuleManager(aliases)

        self.ua_rule.build_rules()
        self.filter_uas()

        # we keep self.selected_ua for testing, mostly
        # TODO: weight
        try:
            self.selected_ua = random.choice(self.filtered_ua_db)
        except IndexError:  # nothing in the list
            raise NoUserAgentFoundException("No user agents matched your filter criteria")
        return self.selected_ua["userAgent"]

    def filter_uas(self):
        for ua_entry in self.ua_db:
            if self._match_criteria(ua_entry):
                self.filtered_ua_db.append(ua_entry)

    def _match_criteria(self, ua_entry: dict) -> bool:
        for criteria in ['platform', 'deviceCategory', 'browser_family']:
            if (getattr(self.ua_rule, criteria) and \
                ua_entry.get(criteria) != getattr(self.ua_rule, criteria)):
                return False

        for search_string in self.ua_rule.search_strings:
            if not search_string in ua_entry.get("userAgent", "").lower():
               return False

        return True


class UARuleManager(object):
    """
    Builds the criteria rules from the user's filter terms and the ua_rules file.
    """

    def __init__(self, aliases:list=None, strmatch:str=None):
        self.strmatch = strmatch
        self.platform = None
        self.deviceCategory = None
        self.browser_family = None
        self.search_strings = []
        self.aliases = [] if None else aliases

    def __str__(self):
        return(f"Rule: platform {self.platform}, deviceCategory {self.deviceCategory}, browser_family: {self.browser_family}, regex {self.search_strings}")

    def build_rules(self):
        used_aliases = []
        all_aliases = list(map(lambda x: x.lower(), self.aliases))

        for rule in ua_rules:
            for alias in all_aliases:
                if alias in map(lambda y: y.lower(), rule["aliases"]):
                    self.set_rule(alias, rule)
                    used_aliases.append(alias)

        for alias in set(all_aliases).difference(set(used_aliases)):
            logger.info(f"** '{alias}' didn't match any known filters, looking for matching browser strings")
            self.search_strings.append(alias)

    def set_rule(self, alias:str, rule:dict) -> None:
        if not self.platform and rule['cat'] == 'platform':
            self.platform = rule['match']
        elif rule['cat'] == 'platform':
            logger.warn("You already have an OS f{self.platform} set and you tried to set "
                        "another, but I'm ignoring it: f{alias}")

        if not self.deviceCategory and rule['cat'] == 'deviceCategory':
            self.deviceCategory = rule['match']
        elif rule['cat'] == 'deviceCategory':
            logger.warn("You already have an OS f{self.platform} set and you tried to set "
                        "another, but I'm ignoring it: f{alias}")

        if not self.browser_family and rule['cat'] == 'browser_family':
            self.browser_family = rule['match']
        elif rule['cat'] == 'browser_family':
            logger.warn("You already have a browser f{self.browser_family} set and you tried to set "
                        "another, but I'm ignoring it: f{alias}")

        if rule.get('regex'):
            self.search_strings.append(rule['regex'])


class UADBManager(object):
    """
    Manages downloading, enriching, updating, and returning the master list
    of user agent definitions.

    The original UA definitions file has some inaccuracies, notably listing
    the vendor as Google everywhere, including for IE. Since it has valuable
    weightings as seen in a user population, we instead do some of our own
    user agent parsing with user_agents for higher accuracy.
    """
    def __init__(self):
        self.db_dir = os.path.join(os.path.expanduser("~"), ".ua-gen-cli/")
        self.raw_db_file_path = os.path.join(self.db_dir, "raw_ua_db.json")
        self.db_file_path = os.path.join(self.db_dir, "enriched_ua_db.json")

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        logger.debug(f"DB file: {self.db_file_path}")

        self.ua_db = []

    def fetch_db(self):
        logger.error("Fetching and enriching user agent DB - we'll be much faster on the next run, scout's honour!")

        r = requests.get(UA_DB_URL, stream=True)

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
                parsed_ua = ua_parse(entry.get("userAgent"))
                entry['browser_family'] = parsed_ua.browser.family
                entry['platform'] = parsed_ua.os.family
                entry['deviceCategory'] = self._get_device_category(parsed_ua)
                entries.append(entry)

            wf.write(json.dumps(entries))

        wf.close()

    def is_too_old(self):
        stat = os.stat(self.db_file_path)
        epoch_now = int(time.time())

        return((epoch_now - stat.st_mtime) > UA_DB_STALE_SECONDS)

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



if __name__ == "__main__":
    args = docopt(__doc__)

    main(args)
