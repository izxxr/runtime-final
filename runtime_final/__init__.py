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

For more details, see: https://runtime-final.readthedocs.io

Copyright (C) I. Ahmad 2022-2023 - Licensed under MIT.
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
    "__version__",
    "__author__",
    "__copyright__",
)

__version__ = "1.1.0"
__author__ = "I. Ahmad (nerdguyahmad)"
__copyright__ = "Copyright (C) I. Ahmad 2022-2023 - Licensed under MIT."


T = TypeVar("T")


def _resolve_target(target: Any) -> Any:
    # This would fail for custom dynamic attributes but there
    # is no way to resolve the underlying function for those
    # attributes; so can't really do anything about it
    if isinstance(target, property):
        return target.fget
    if isinstance(target, (staticmethod, classmethod)):
        return target.__func__
    return target


@classmethod
def _forbid_subclassing(cls: Any) -> NoReturn:
    raise RuntimeError(f"Cannot subclass the final class {cls.__name__!r}")


@classmethod
def _forbid_overriding_finals(cls: Any) -> Union[NoReturn, None]:
    final_methods: Set[str] = getattr(cls, "__runtime_final_methods__", set())  # type: ignore
    overrides = vars(cls)

    for name in final_methods:
        if name in overrides:
            raise RuntimeError(f"Cannot override {name!r} in class {cls.__name__!r}")

    old_init_subclass = getattr(cls, "__runtime_old_init_subclass__", None)
    if old_init_subclass:
        old_init_subclass()


def get_final_methods(target: type) -> Tuple[Callable[..., Any], ...]:
    """Gets the final methods of given class.

    Parameters
    ----------
    target: :class:`type`
        The class to get final methods for.

    Returns
    -------
    :class:`tuple`
        The tuple of function objects that are marked as final.
    """
    if not hasattr(target, "__runtime_final_methods__"):
        return ()
    return tuple((getattr(target, name) for name in target.__runtime_final_methods__))  # type: ignore


def is_final(target: Any) -> bool:
    """Indicates whether a class or function is declared as final.

    Parameters
    ----------
    target:
        The class or method to check for.

    Returns
    -------
    :class:`bool`
    """
    return hasattr(target, "__runtime_is_final__")


class _Final:
    if TYPE_CHECKING:
        __original_target__: Any
        __target__: Any

    def __new__(cls, target: Any) -> Any:
        cls.__original_target__ = target
        cls.__target__ = _resolve_target(target)
        cls.__target__.__runtime_is_final__ = True

        if inspect.isclass(target):
            # Unlike methods, classes don't need any extra working
            # so no need to call super().__new__()
            cls.__target__.__init_subclass__ = _forbid_subclassing
            return target

        return super().__new__(cls)

    def __init__(self, target: Any) -> None:
        # __target__ is set during __new__() so we don't have
        # to do anything here. This constructor primarily exists to
        # avoid errors
        pass

    def __set_name__(self, owner: Any, name: str) -> None:
        cls = self.__class__
        if hasattr(owner, "__runtime_final_methods__"):
            owner.__runtime_final_methods__.add(name)
        else:
            owner.__runtime_final_methods__ = {name}

        owner.__runtime_old_init_subclass__ = owner.__init_subclass__
        owner.__init_subclass__ = _forbid_overriding_finals
        setattr(owner, name, cls.__original_target__)


if TYPE_CHECKING:
    def final(target: T) -> T:
        """A decorator that declares a class or method as final."""
        ...
else:
    def final(target) -> _Final:
        """A decorator that declares a class or method as final.

        A class declared as final with this decorator cannot
        be subclassed by other classes. Similarly, when methods
        of a class are declared as final, The subclasses cannot
        override them.

        Trying to subclass final classes or overriding final
        methods will raise :exc:`RuntimeError`.

        Here is an example of final classes::

            @final
            class User:
                pass

            # The following line will raise RuntimeError
            class SpecialUser(User):
                pass

        And final methods::

            class User:
                @final
                def delete(self):
                    pass

            class SpecialUser(User):
                # The following line will raise RuntimeError
                def delete(self):
                    pass

        .. note::

            When using this decorator with special attributes such as :func:`staticmethod`,
            :func:`classmethod` and :func:`property`, This decorator should be placed
            *above* the relevant decorator for that special attribute.

            E.g::

                # Correct:
                @final
                @property
                def foo(self):
                    ...

                # Wrong:
                @property
                @final
                def foo(self):
                    ...

        This decorator is also fully compatible with the :func:`typing.final`.
        In applications where type checkers need to understand the usage of
        final decorator, the ``typing.TYPE_CHECKING`` constant can be used::

            from typing import TYPE_CHECKING

            if TYPE_CHECKING:
                # Type checkers will consider this clause but
                # this will not execute at runtime.
                from typing import final
            else:
                # Type checkers will ignore this clause but
                # this is always executed at runtime.
                from runtime_final import final
        """
        return _Final(target)
