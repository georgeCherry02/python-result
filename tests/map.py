from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from result import Result

import pytest


T = TypeVar("T")
T_PRIME = TypeVar("T_PRIME")


@dataclass
class TestCase(Generic[T, T_PRIME]):
    initial_value: T
    mapping: Callable[[T], T_PRIME]
    expected_output: T_PRIME

    __test__ = False

    def __str__(self) -> str:
        return f"[input: {self.initial_value}, output: {self.expected_output}]"


SIMPLE_TESTCASES = [
    TestCase(5, lambda x: x + 1, 6),
    TestCase("Hello", lambda x: f"{x} World", "Hello World"),
    TestCase(5, lambda x: str(x), "5"),
]

@pytest.mark.parametrize(("testcase"), argvalues=SIMPLE_TESTCASES)
def test_simple_mapping(testcase: TestCase):
    r = Result.Ok(testcase.initial_value)
    o = r.map(testcase.mapping)
    assert o.is_ok(), "Mapping failed to sustain expected case"
    assert o.unwrap() == testcase.expected_output, f"Mapping failed to yield expected output, testcase={testcase}"
