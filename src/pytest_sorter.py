# -*- coding: utf-8 -*-
import json
import os
from collections import defaultdict

import pytest

__version__ = '0.2.1'


FILENAME = '.test_history'


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption('--no-sorted', action='store_true', dest='no_sorted',
                     help="Run the tests in sorted order")


@pytest.mark.trylast
def pytest_configure(config):
    config_line = (
        'historical: set the historical executions and fails count '
        'for a specific test. Provided by pytest-src. '
    )
    config.addinivalue_line('markers', config_line)

    if not config.option.no_sorted:
        if config.pluginmanager.hasplugin('xdist'):
            if hasattr(config, 'workerinput'):
                worker_id = config.workerinput['workerid']
                config.pluginmanager.register(TestSorterWorker(config, worker_id), "using-src-worker")
            else:
                config.pluginmanager.register(TestSorterXDist(config), "using-src")
        else:
            config.pluginmanager.register(TestSorter(config), "using-src")


class TestSorter(object):

    def __init__(self, config):
        self.config = config
        self.test_history = defaultdict(str)
        self.path = config.rootdir.strpath
        self.path = (self.path + '/') if self.path[-1] != '/' else self.path
        self.load_test_history()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        callinfo = yield
        if call.when == 'call':
            test_name = self.get_test_name(item)
            outcome = callinfo.get_result().outcome
            self.register_test_run(test_name, outcome)

    @pytest.mark.trylast
    def pytest_unconfigure(self, config):
        self.save_test_history()

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
        """ Real meat for the plugin. Here the tests are sorted by their historic value """
        items_value = []

        for item in items:
            test_name = self.get_test_name(item)

            # GET EXECUTION AND FAIL COUNT FROM MARKS
            mark = self.get_historical_marker_from_item(item)
            plus_exec = 0
            plus_fail = 0
            if mark is not None:
                plus_exec = abs(mark.kwargs.get('execs', 0))
                plus_fail = abs(mark.kwargs.get('fails', 0))

            # CALCULATE TEST VALUE USING HISTORIC AND MARK VALUES
            items_value.append({
                'item': item,
                'value': self.get_test_order_value(
                    test_name,
                    plus_exec=plus_exec,
                    plus_fail=plus_fail
                )
            })

        # SORT ITEMS BY THEIR VALUE
        sorted_items = [test_dict['item'] for test_dict in sorted(items_value, reverse=True, key=lambda x: x['value'])]
        items[:] = sorted_items

    @property
    def file(self):
        return self.path + FILENAME

    def get_historical_marker_from_item(self, item):
        """ Extract the pytest-src 'historial' marker from a item """
        for mark in item.own_markers:
            if mark.name == 'historical':
                return mark
        return None

    def get_test_order_value(self, test_name, plus_exec=0, plus_fail=0):
        if test_name not in self.test_history.keys():
            exec_count, fail_count = 0, 0
        else:
            exec_count, fail_count = self.test_history[test_name]
        if (exec_count + plus_exec) <= 0:
            return 0
        return (fail_count + plus_fail) / (exec_count + plus_exec)

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
        except Exception as e:
            print("\ncould not save tests history to {}".format(self.file))
            print(e)

    def register_test_run(self, test_name, outcome):
        if outcome == 'skipped':
            return
        failed = outcome == 'failed'
        if test_name not in self.test_history.keys():
            self.test_history[test_name] = [0, 0]
        self.test_history[test_name][0] += 1
        self.test_history[test_name][1] = (self.test_history[test_name][1] + 1) if failed else self.test_history[test_name][1]

    def get_test_name(self, item):
        from pytest import Module
        if isinstance(item, Module):
            return item.nodeid
        return item.location[0] + "::" + item.location[2]


class TestSorterWorker(TestSorter):

    def __init__(self, config, worker_id):
        self.worker_id = worker_id
        super(TestSorterWorker, self).__init__(config)

    @property
    def file(self):
        return self.path + ".results_" + self.worker_id

    @pytest.mark.tryfirst
    def pytest_unconfigure(self, config):
        self.save_test_history()


class TestSorterXDist(TestSorter):

    @pytest.mark.trylast
    def pytest_unconfigure(self, config):
        pytest_sorter = config.pluginmanager.getplugin("using-src")
        path = pytest_sorter.path
        # IT's the main node. must save aggregated test infos from all workers
        plugin = config.pluginmanager.getplugin("dsession")
        if plugin:
            for spec in plugin.trdist._specs:
                workerid = spec.id
                with open(path + '.results_' + workerid, 'r') as f:
                    loaded = json.load(f)
                for test_name, data in loaded.items():
                    outcome = 'failed' if data[1] > 0 else 'passed'
                    self.register_test_run(test_name, outcome)
                os.remove(path + '.results_' + workerid)
            self.save_test_history()
