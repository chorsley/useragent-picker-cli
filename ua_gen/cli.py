"""uagen - generate realistic, filtered browser useragents.

Usage:
  uagen
  uagen [--force-update-db] FILTER...
  uagen --list-filters
  uagen (-h | --help)
  uagen --version

Arguments:
  FILTER...
              Give a number of keyword filters like 'win', 'firefox'

Options:
  --force-update-db  Force an update of the UA DB cache
  --list-filters     Show all available useragent aliases
  -h --help          Show this screen.
  --version          Show version.
"""

import os.path
import os
import random
import re
import sys

from docopt import docopt

from . import ua_rules
from . import consts as c

from .logging import logger
from .db_manager import UADBManager
from .exceptions import NoUserAgentFoundException


class UAGen(object):
    def __init__(self, ua_db:UADBManager=None, force_db_update:bool=False):
        # normal operation
        if not ua_db:
            self.db_manager = UADBManager(force_db_update=force_db_update)
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
        return self.selected_ua[c.UA_USERAGENT]

    def filter_uas(self):
        for ua_entry in self.ua_db:
            if self._match_criteria(ua_entry):
                self.filtered_ua_db.append(ua_entry)

    def _match_criteria(self, ua_entry: dict) -> bool:
        for criteria in [c.UA_PLATFORM, c.UA_DEVICE_CATEGORY, c.UA_BROWSER_FAMILY]:
            if (getattr(self.ua_rule, criteria) and \
                ua_entry.get(criteria) != getattr(self.ua_rule, criteria)):
                return False

        for search_string in self.ua_rule.search_strings:
            if not search_string in ua_entry.get(c.UA_USERAGENT, "").lower():
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
        self.browserFamily = None
        self.search_strings = []
        self.aliases = [] if None else aliases

    def __str__(self):
        return(f"Rule: platform {self.platform}, deviceCategory {self.deviceCategory}, browserFamily: {self.browserFamily}, regex {self.search_strings}")

    def build_rules(self):
        used_aliases = []
        all_aliases = list(map(lambda x: x.lower(), self.aliases))

        for alias in all_aliases:
            for rule in ua_rules:
                if alias in map(lambda y: y.lower(), rule["aliases"]):
                    self.set_rule(alias, rule)
                    used_aliases.append(alias)

        for alias in set(all_aliases).difference(set(used_aliases)):
            logger.info(f"** '{alias}' didn't match any known filters, looking for matching browser strings")
            self.search_strings.append(alias)

    def set_rule(self, alias:str, rule:dict) -> None:
        """
        Based on properties set so far in UARuleManager, set as many filter criteria as we have.

        If two rules try to set the same thing (e.g. safari + firefox or ios + android, ignore the second and warn)
        """
        if not self.platform and rule['cat'] == c.UA_PLATFORM:
            self.platform = rule['match']
        elif rule['cat'] == c.UA_PLATFORM:
            logger.warning(f"* You already have an OS ({self.platform}) set and you tried to set "
                           f"another, so I'm ignoring '{alias}'")
        if not self.deviceCategory and rule['cat'] == c.UA_DEVICE_CATEGORY:
            self.deviceCategory = rule['match']
        elif rule['cat'] == c.UA_DEVICE_CATEGORY:
            logger.warning(f"* You already have an device type ({self.deviceCategory}) set and you tried to set "
                           f"another, so I'm ignoring '{alias}'")

        if not self.browserFamily and rule['cat'] == c.UA_BROWSER_FAMILY:
            self.browserFamily = rule['match']
        elif rule['cat'] == c.UA_BROWSER_FAMILY:
            logger.warning(f"* You already have a browser family ({self.browserFamily}) set and you tried to set "
                           f"another, so I'm ignoring '{alias}'")

        if rule.get('regex'):
            self.search_strings.append(rule['regex'])


def show_aliases():
    print("These filters and filter aliases are supported by uagen:")

    heading = None

    for rule in ua_rules:
        head_candidate = c.UA_PROP_LABELS.get(rule['cat'])
        if heading != head_candidate:
            print(f"\n{head_candidate}")
            heading = head_candidate

        print(f"   {rule['match']}  [{', '.join(rule['aliases'])}]")

    print("\nUse can also use useragent filters that aren't in this list - uagen will just search useragent strings for them.")


def start_uagen(args):
    """Generates random but realistic user agents on a command line (or via API)"""

    if args["--list-filters"]:
        show_aliases()
    else:
        uagen = UAGen(force_db_update=bool(args["--force-update-db"]))

        try:
            print(uagen.get_ua(aliases=args["FILTER"]))
        except NoUserAgentFoundException:
            logger.error("Sorry, I couldn't find any user agents matching your criteria.\n")
            logger.error("Remember, the UA list contains agents seen in the wild, so if you want something very exotic, ")
            logger.error("you might need to go and find it elsewhere.") 
            sys.exit(1)


def main():
    args = docopt(__doc__)

    start_uagen(args)


if __name__ == "__main__":
    main()