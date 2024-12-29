from __future__ import annotations

from typing import Callable, Generic, NoReturn, Optional, Protocol, TypeVar, Union
from typing_extensions import TypeGuard


class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...


T = TypeVar("T")
T_PRIME = TypeVar("T_PRIME")
U = TypeVar("U", bound=SupportsStr)
U_PRIME = TypeVar("U_PRIME", bound=SupportsStr)


class ResultError(Exception):
    """
    This error is a wrapper around a raised error from a `Result` chain
    """
    def __init__(self, message: SupportsStr):
        message = str(message)
        super().__init__(message)


class InvalidResultStateError(Exception):
    """
    This error represents a result that has reached an invalid state
    """
    def __init__(self, result: Result):
        self.message = str(result)
        super().__init__(self.message)


class Result(Generic[T, U]):
    def __init__(self, exp: Optional[T], err: Optional[U]):
        self._exp: Optional[T] = exp
        self._err: Optional[U] = err
        if not self._valid_state():
            raise InvalidResultStateError(self)

    @staticmethod
    def Ok(expected: T) -> Result[T, U]:
        return Result(exp=expected, err=None)

    @staticmethod
    def Err(error: U) -> Result[T, U]:
        return Result(exp=None, err=error)

    def _is_expected_state(self, exp: Optional[T]) -> TypeGuard[T]:
        return exp is not None and self._err is None

    def is_ok(self) -> bool:
        return self._is_expected_state(self._exp)

    def _is_errored_state(self, err: Optional[U]) -> TypeGuard[U]:
        return err is not None and self._exp is None

    def is_err(self) -> bool:
        return self._is_errored_state(self._err)

    def _valid_state(self) -> bool:
        return self._is_expected_state(self._exp) or self._is_errored_state(self._err)

    def __repr__(self) -> str:
        return f"Result(exp={self._exp!r}, err={self._err!r})"

    def __str__(self) -> str:
        if self._is_expected_state(self._exp):
            return f"Ok({self._exp})"
        elif self._is_errored_state(self._err):
            return f"Err({self._err})"
        else:
            return f"Invalid Result: [exp={self._exp}, err={self._err}]"

    def map(self, func: Callable[[T], T_PRIME]) -> Result[T_PRIME, U]:
        ResultT = Result[T_PRIME, U]
        if self._is_expected_state(self._exp):
            return ResultT.Ok(func(self._exp))
        elif self._is_errored_state(self._err):
            return ResultT.Err(self._err)
        else:
            raise InvalidResultStateError(self)

    def and_then(self, func: Callable[[T], Result[T_PRIME, U]]) -> Result[T_PRIME, U]:
        ResultT = Result[T_PRIME, U]
        if self._is_expected_state(self._exp):
            return func(self._exp)
        elif self._is_errored_state(self._err):
            return ResultT.Err(self._err)
        else:
            raise InvalidResultStateError(self)

    def map_err(self, func: Callable[[U], U_PRIME]) -> Result[T, U_PRIME]:
        ResultT = Result[T, U_PRIME]
        if self._is_errored_state(self._err):
            return ResultT.Err(func(self._err))
        elif self._is_expected_state(self._exp):
            return ResultT.Ok(self._exp)
        else:
            raise InvalidResultStateError(self)

    def or_else(self, func: Callable[[U], Result[T, U_PRIME]]) -> Result[T, U_PRIME]:
        ResultT = Result[T, U_PRIME]
        if self._is_errored_state(self._err):
            return func(self._err)
        elif self._is_expected_state(self._exp):
            return ResultT.Ok(self._exp)
        else:
            raise InvalidResultStateError(self)

    def if_error_raise_wrapped(self) -> Result[T, U]:
        if self._is_errored_state(self._err):
            raise ResultError(self._err)
        return self

    def if_error_raise_direct(self) -> Result[T, U]:
        if self._is_errored_state(self._err) and isinstance(self._err, Exception):
            raise self._err
        return self

    def if_error_raise(self) -> Result[T, U]:
        if self._is_errored_state(self._err):
            if isinstance(self._err, Exception):
                raise self._err
            else:
                raise ResultError(self._err)
        else:
            return self

    def unwrap(self) -> T:
        self.if_error_raise()
        if self._is_expected_state(self._exp):
            return self._exp
        else:
            raise InvalidResultStateError(self)

    def unwrap_or(self, default_value: T) -> T:
        if self._is_expected_state(self._exp):
            return self._exp
        elif self._is_errored_state(self._err):
            return default_value
        else:
            raise InvalidResultStateError(self)
