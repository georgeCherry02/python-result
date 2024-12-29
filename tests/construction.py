from typing import Optional
import pytest

from result import Result, ResultState, InvalidResultStateError

from tests.stubs import Foo


def test_explicit_expected_initialization():
    Result(5, None, ResultState.Expected)


def test_explicit_unexpected_initialization():
    Result(None, "Failure", ResultState.Errored)


def test_expected_helper_initialization():
    r = Result.Ok(5)
    assert isinstance(r, Result), "Result failed to construct at all"
    assert r._exp == 5, "Result.Ok(5) failed to instantiate expected value of 5"
    assert r._err is None, "Result.Ok(5) failed to instantiate errored value of None"
    assert r._state == ResultState.Expected, "Result.Ok(5) failed to instantiate state to Expected"


def test_expected_helper_initialization_custom_class():
    r = Result.Ok(Foo(5))
    assert isinstance(r, Result), "Result failed to construct at all"
    assert r._exp is not None, "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5)"
    assert r._exp.a == 5, "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5)"
    assert r._exp == Foo(5), "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5)"
    assert r._exp == 5, "Result.Ok(Foo(5)) failed to instantiate expected value of Foo(5) and preserve behaviour"
    assert r._err is None, "Result.Ok(Foo(5)) failed to instantiate errored value of None"
    assert r._state == ResultState.Expected, "Result.Ok(Foo(5)) failed to instantiate state to Expected"


def test_errored_helper_initialization():
    r = Result.Err("Errored")
    assert isinstance(r, Result), "Result failed to construct at all"
    assert r._exp is None, 'Result.Err("Errored") failed to instantiate expected value of None'
    assert r._err == "Errored", 'Result.Err("Errored") failed to instantiate an errored value of "Errored"'
    assert r._state == ResultState.Errored, 'Result.Err("Errored") failed to instantiate state to Errored'


def test_optional_expected_explicit_initialization():
    Result[Optional[int], str](None, None, ResultState.Expected)


def test_optional_expected_helper_initialization():
    r = Result.Ok(None)
    assert isinstance(r, Result), "Result failed to construct at all"
    assert r._exp is None, "Result.Ok(None) failed in instantiate Expected[Optional]"
    assert r._err is None, "Result.Ok(None) failed to instantiate errored value to None"
    assert r._state == ResultState.Expected, "Result.Ok(None) failed to instantiate state to Expected"


def test_both_populated_initialization():
    with pytest.raises(InvalidResultStateError) as err:
        Result(5, 5, ResultState.Errored)
    assert str(err.value) == "Invalid state: Result(exp=5, err=5, state=ResultState.Errored)", "Failed initialization of [5, 5] incorrectly"
