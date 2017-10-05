import pytest
from pprint import pprint
from collections import defaultdict
import json

def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption('--no-sorted', action='store_true', dest='no_sorted',
                     help="Run the tests in sorted order")

def pytest_configure(config):
    config_line = (
        'historical: set the historical executions and fails count '
        'for a specific test. Provided by pytest-sorter. '
    )
    config.addinivalue_line('markers', config_line)

    if config.option.no_sorted:
        return

    from tests.conftest import TestSorter
    test_sorter = TestSorter(config)
    config.pluginmanager.register(test_sorter, "test_sorter")
