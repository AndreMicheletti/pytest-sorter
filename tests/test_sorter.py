# -*- coding: utf-8 -*-
import re
from pprint import pprint
import pytest

pytest_plugins = ['pytester']

@pytest.fixture
def item_names_for(testdir):

    def _item_names_for(tests_content):
        # some strange code to extract sorted items
        items = testdir.getitems(tests_content)
        config = testdir.config

        from conftest import TestSorter
        test_sorter = TestSorter(config)

        hook = testdir.config.hook
        hook.pytest_collection_modifyitems(session=items[0].session,
                                           config=config, items=items)
        return [item.name for item in items]

    return _item_names_for


def test_no_marks(item_names_for):
    tests_content = """
    def test_1(): pass
    def test_2(): pass
    """

    assert item_names_for(tests_content) == ['test_1', 'test_2']


def test_marks(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.historical(execs=10, fails=0)
    def test_1():
        pass

    @pytest.mark.historical(execs=10, fails=10)
    def test_2():
        pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_1']


def test_marks_and_no_marks(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.historical(execs=10, fails=4)
    def test_1():
        pass

    @pytest.mark.historical(execs=10, fails=10)
    def test_2():
        pass

    def test_3():
        pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_1', 'test_3']


def test_relative_score(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.historical(execs=110, fails=40)
    def test_1():
        pass

    @pytest.mark.historical(execs=70, fails=50)
    def test_2():
        pass

    @pytest.mark.historical(execs=10, fails=0)
    def test_3():
        pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_1', 'test_3']


def test_marks_parametize(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.historical(execs=10, fails=4)
    def test_1():
        pass

    @pytest.mark.historical(execs=10, fails=10)
    @pytest.mark.parametrize(
        "test_input,expected",
        [(3, 3), (4, 4), (6, 6)])
    def test_eval(test_input, expected):
        assert eval(test_input) == expected
    """

    assert item_names_for(tests_content) == ['test_eval[3-3]', 'test_eval[4-4]', 'test_eval[6-6]', 'test_1']
