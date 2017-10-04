# -*- coding: utf-8 -*-
import pytest

@pytest.fixture
def item_names_for(testdir):

    def _item_names_for(tests_content):
        # some strange code to extract sorted items
        items = testdir.getitems(tests_content)
        hook = testdir.config.hook
        hook.pytest_collection_modifyitems(session=items[0].session,
                                           config=testdir.config, items=items)
        return [item.name for item in items]

    return _item_names_for

@pytest.fixture(params=[True, True, True, True, True, False, True])
def a_thousand_tests(request):
    return request.param

def test_should_be_last(a_thousand_tests):
    import time
    time.sleep(1)
    assert True

def test_will_fail(item_names_for):
    import time
    time.sleep(5)
    assert False
