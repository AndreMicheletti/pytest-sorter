# -*- coding: utf-8 -*-

import pytest

def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group._addoption('--sorted', action='store', metavar='path', default=None,
                     help="Run the tests in sorted order")

@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    config._sorter = TestSorter(config)


def pytest_unconfigure(config):
    if hasattr(config, '_sorter'):
        # write summary
        config._sorter.write_file()


def pytest_collection_modifyitems(session, config, items):
    print("ITEMS COLLECTED ", items)


class TestSorter(object):

    def __init__(self, config):
        self.config = config

    def write_file(self):
        """
        Creates a new file with pytest session contents.
        :contents: pytest stdout contents
        """
        path = self.config.option.sorted
        with open(path+'myfile.andre', 'w') as f:
            f.writelines(str(self.config))
