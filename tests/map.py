from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from result import Result

from tests.stubs import Foo

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
    TestCase(None, lambda _: "Hello", "Hello"),
    TestCase("Hello", lambda _: None, None)
]

@pytest.mark.parametrize(("testcase"), argvalues=SIMPLE_TESTCASES)
def test_simple_mapping(testcase: TestCase):
    r = Result.Ok(testcase.initial_value)
    o = r.map(testcase.mapping)
    assert o.is_ok(), "Mapping failed to sustain expected case"
    assert o.unwrap() == testcase.expected_output, f"Mapping failed to yield expected output, testcase={testcase}"

def test_chained_mapping():
    r = Result.Ok("Hello")
    o = r.map(lambda s: f"{s} World") \
            .map(lambda s: s.split(" ")) \
            .map(lambda list_of_strings: (l.lower() for l in list_of_strings)) \
            .map(lambda generator_of_strings: " ".join(generator_of_strings))

    assert o.is_ok(), "Mapping failed to chain operations"
    assert o.unwrap() == "hello world", "Chain of mappings failed to yield expected output"

def test_in_place_mutation():
    r = Result.Ok(Foo(5))
    o = r.map_member(Foo.increment)

    assert o.is_ok(), "Mapping failed outright for mutation"
    assert o.unwrap() == Foo(6), "Mapping failed to mutate value inplace"
