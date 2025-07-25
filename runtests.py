#!/usr/bin/env python
import argparse
import os
import sys

import django
from django.core.exceptions import ImproperlyConfigured
from django.test.runner import DiscoverRunner
from django.test.selenium import SeleniumTestCaseBase


# Copied from django/tests/runtests.py
class ActionSelenium(argparse.Action):
    """
    Validate the comma-separated list of requested browsers.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            import selenium  # NOQA
        except ImportError as e:
            raise ImproperlyConfigured(f"Error loading selenium module: {e}")
        browsers = values.split(",")
        for browser in browsers:
            try:
                SeleniumTestCaseBase.import_webdriver(browser)
            except ImportError:
                raise argparse.ArgumentError(
                    self, f"Selenium browser specification {browser} is not valid."
                )
        setattr(namespace, self.dest, browsers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--selenium",
        action=ActionSelenium,
        metavar="BROWSERS",
        help="A comma-separated list of browsers to run the Selenium tests against.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run selenium tests in headless mode, if the browser supports the option.",
    )
    parser.add_argument(
        "--screenshots",
        action="store_true",
        help="Take screenshots during selenium tests to capture the user interface.",
    )
    options = parser.parse_args()

    if options.screenshots and not options.selenium:
        parser.error("--screenshots require --selenium to be used.")

    SeleniumTestCaseBase.browsers = options.selenium
    SeleniumTestCaseBase.headless = options.headless
    SeleniumTestCaseBase.screenshots = options.screenshots

    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    django.setup()
    test_runner = DiscoverRunner(verbosity=3)
    failures = test_runner.run_tests([])
    sys.exit(failures)


if __name__ == "__main__":
    main()
