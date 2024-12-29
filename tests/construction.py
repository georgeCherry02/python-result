import pytest
from result import Result, InvalidResultStateError

from tests.stubs import Foo


def test_explicit_expected_construction():
    Result(5, None)


def test_explicit_unexpected_construction():
    Result(None, "Failure")


def test_expected_helper_initialization():
    r = Result.Ok(5)
    assert isinstance(r, Result), "Result failed to construct at all"
    assert r._exp == 5, "Result.Ok(5) failed to instantiate expected value of 5"
    assert r._err is None, "Result.Ok(5) failed to instantiate errored value of None"


def test_expected_helper_initialization_custom_class():
    r = Result.Ok(Foo(5))
    assert isinstance(r, Result), "Result failed to construct at all"
    assert r._exp is not None, "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5)"
    assert r._exp.a == 5, "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5)"
    assert r._exp == Foo(5), "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5)"
    assert r._exp == 5, "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5) and preserve behaviour"
    assert r._err is None, "Result.Ok(Foo(5)) failed to instantiate errored value of None"


def test_errored_helper_initialization():
    r = Result.Err("Errored")
    assert isinstance(r, Result), "Result failed to construct at all"
    assert r._exp is None, 'Result.Err("Errored") failed to instantiate expected value of None'
    assert r._err == "Errored", 'Result.Err("Errored") failed to instantiate an errored value of "Errored"'


def test_both_none_construction():
    with pytest.raises(InvalidResultStateError) as err:
        Result(None, None)
    assert str(err.value) == "Invalid Result: [exp=None, err=None]", "Failed construction of [None, None] incorrectly"


def test_both_populated_construction():
    with pytest.raises(InvalidResultStateError) as err:
        Result(5, 5)
    assert str(err.value) == "Invalid Result: [exp=5, err=5]", "Failed construction of [5, 5] incorrectly"
