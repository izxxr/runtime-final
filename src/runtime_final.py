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

Refactored by gentlegiantJGC
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
)
import inspect

__version__ = "1.1.0"
__author__ = "gentlegiantJGC and I. Ahmad (izxxr)"
__copyright__ = "Copyright (C) I. Ahmad 2022-2023 - Licensed under MIT."


@classmethod
def _forbid_subclassing(cls):
    raise RuntimeError(f"Cannot subclass the final class {cls.__name__!r}")


class _Final:
    def __init__(self, target: Any):
        self.__target = target

    def __set_name__(self, owner: Any, name: str):
        """Called when the method is assigned its name in the class"""
        if not hasattr(owner, "__runtime_final_methods__"):
            # If the class has not already been patched, patch it.
            # A dictionary mapping the name to the class it was finalised in. Dict[str, str]
            owner.__runtime_final_methods__ = {}
            old_init_subclass = owner.__init_subclass__

            @classmethod
            def _forbid_overriding_finals(cls):
                final_methods: Dict[str, str] = cls.__runtime_final_methods__
                overrides = vars(cls)

                for name in final_methods:
                    # The class defines a method that was finalised in a different class
                    if (
                        name in overrides
                        and final_methods[name] != f"{cls.__module__}.{cls.__name__}"
                    ):
                        raise RuntimeError(
                            f"Cannot override {name!r} in class {cls.__name__!r}"
                        )

                if old_init_subclass:
                    old_init_subclass()

            owner.__init_subclass__ = _forbid_overriding_finals

        if name in owner.__runtime_final_methods__:
            # If the method has been finalised
            raise RuntimeError(f"Cannot override {name!r} in class {owner.__name__!r}")
        owner.__runtime_final_methods__[name] = f"{owner.__module__}.{owner.__name__}"
        setattr(owner, name, self.__target)

    def __call__(self, *args, **kwargs):
        raise RuntimeError(
            "The final decorator only works on methods assigned in a class."
        )


if TYPE_CHECKING:
    from typing import final
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
        if inspect.isclass(target):
            target.__final__ = True
            target.__init_subclass__ = _forbid_subclassing
            return target
        elif inspect.isfunction(target):
            target.__final__ = True
            return _Final(target)
        elif isinstance(target, (property, staticmethod, classmethod)):
            return _Final(target)
        else:
            raise RuntimeError(
                "The final decorator can only be used with classes and methods."
            )
