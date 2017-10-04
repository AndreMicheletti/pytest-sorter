# -*- coding: utf-8 -*-
import pytest
from pprint import pprint
from collections import defaultdict
import json

def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption('--sorted', action='store_true', dest='sorted',
                     help="Run the tests in sorted order")

def pytest_configure(config):
    if not config.option.sorted:
        return
    test_sorter = TestSorter(config)
    config.pluginmanager.register(test_sorter, "test_sorter")


class TestSorter(object):

    def __init__(self, config):
        self.config = config
        self.test_history = defaultdict(str)
        self.file = config.args[0] + '/.test_history'
        self.load_test_history()

    def get_test_name(self, item):
        return item.location[0] + "::" + item.location[2]

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        callinfo = yield
        if call.when == 'call':
            test_name = self.get_test_name(item)
            outcome = callinfo.result.outcome
            self.register_test_run(test_name, outcome)

    def pytest_unconfigure(self, config):
        self.save_test_history()

    def get_test_value(self, test_name):
        if test_name not in self.test_history.keys():
            return 0
        info = self.test_history[test_name]
        exec_count, fail_count = [int(value) for value in info.split(",")]
        if (exec_count == 0):
            return 0
        return fail_count / exec_count

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
        items_value = []
        for item in items:
            test_name = self.get_test_name(item)
            print("FOUND ", test_name)
            items_value.append({
                'item': item,
                'value': self.get_test_value(test_name)
            })
        sorted_items = [test_dict['item'] for test_dict in sorted(items_value, reverse=True, key=lambda x: x['value'])]
        print("SORTED ")
        pprint(sorted_items)
        items[:] = sorted_items

    def load_test_history(self):
        try:
            with open(self.file, 'r') as f:
                self.test_history = json.load(f)
        except:
            self.save_test_history()

    def save_test_history(self):
        try:
            with open(self.file, 'w') as f:
                json.dump(self.test_history, f)
        except:
            print("\ncould not save tests history to {}".format(self.file))

    def register_test_run(self, test_name, outcome):
        if outcome == 'skipped':
            return
        failed = outcome == 'failed'
        if test_name not in self.test_history.keys():
            self.test_history[test_name] = '0,0'
        info = self.test_history[test_name]
        if info != '':
            exec_count, fail_count = [int(value) for value in info.split(",")]
        else:
            exec_count, fail_count = 0, 0
        exec_count += 1
        fail_count = (fail_count + 1) if failed else fail_count
        self.test_history[test_name] = "{},{}".format(exec_count, fail_count)
