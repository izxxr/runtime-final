"""Final classes and methods at runtime.

This module provides a decorator interface to declare final
classes and methods.

This module is inspired by and is compatible with `typing.final`.
See PEP-591 (https://www.python.org/dev/peps/pep-0591) for more
details on this topic.

The main component of this module is the `final` decorator that
can be used to decorate classes and methods inside a class. As
such:

- Classes decorated with @final cannot be subclassed.
- Methods decorated with @final cannot be overriden in subclasses.

Example usage (classes)::

    from runtime_final import final

    @final
    class Foo:
        ...
    
    class Bar(Foo):  # Raises RuntimeError
        ...

Example usage (methods)::

    from runtime_final import final

    class User:
        @final
        def edit(self):
            ...
    
    class AnotherUser(User):
        def edit(self):  # Raises RuntimeError
            ...

This module is also compatible with the `final` decorator
provided by the typing module from standard library. You
can easily combine this module with typing module::

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from typing import final
    else:
        from runtime_final import final

`typing.TYPE_CHECKING` is always False at runtime while is True
for type checkers.

For more details, see: https://github.com/nerdguyahmad/runtime-final

Copyright (C) Izhar Ahmad 2022-2023 - Licensed under MIT.
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    NoReturn,
    Set,
    Union,
    Tuple,
    TypeVar,
)
import inspect


__all__ = (
    "final",
    "get_final_methods",
    "is_final",
)


TargetType = Union[Callable[..., Any], type]
T = TypeVar("T", bound=TargetType)


@classmethod
def _forbid_subclassing(cls: Any) -> NoReturn:
    raise RuntimeError(f"Cannot subclass the final class {cls.__name__!r}")


@classmethod
def _forbid_overriding_finals(cls: Any) -> Union[NoReturn, None]:
    final_methods: Set[str] = getattr(cls, "__runtime_final_methods__", set[str]())
    overrides = vars(cls)
    old_init_subclass = getattr(cls, "__runtime_old_init_subclass__", None)

    for name in final_methods:
        if name in overrides:
            raise RuntimeError(f"Cannot override {name!r} in class {cls.__name__!r}")
    
    if old_init_subclass:
        old_init_subclass()


def get_final_methods(target: type) -> Tuple[Callable[..., Any], ...]:
    """Gets the final methods of given class.
    
    Returns the tuple of function objects that are marked
    as final in the given class.
    """
    if not hasattr(target, "__runtime_final_methods__"):
        return ()
    return tuple((getattr(target, name) for name in target.__runtime_final_methods__))  # type: ignore


def is_final(target: TargetType) -> bool:
    """Indicates whether a class or function is declared as final."""
    return hasattr(target, "__runtime_is_final__")


class _Final:
    """A decorator that declares a class or method as final.
    
    For more information about how this works, Consider
    seeing this module's docstring.
    """
    # Most type ignores in this class are because of runtime assignments

    def __new__(cls, target: TargetType) -> Any:
        if inspect.isclass(target):
            target.__init_subclass__ = _forbid_subclassing  # type: ignore
            target.__runtime_is_final__ = True  # type: ignore
            return target
            
        return super().__new__(cls)
    
    def __init__(self, target: TargetType) -> None:
        self.target = target
        target.__runtime_is_final__ = True  # type: ignore

    def __set_name__(self, owner: type, name: str) -> None:
        target = self.target
        if hasattr(owner, "__runtime_final_methods__"):
            owner.__runtime_final_methods__.add(target.__name__)  # type: ignore
        else:
            owner.__runtime_final_methods__ = {target.__name__}  # type: ignore
        
        owner.__runtime_old_init_subclass__ = owner.__init_subclass__  # type: ignore
        owner.__init_subclass__ = _forbid_overriding_finals  # type: ignore
        setattr(owner, name, target)


if TYPE_CHECKING:
    def final(target: T) -> T:
        ...
else:
    def final(target) -> None:
        return _Final(target)
