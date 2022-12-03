"""
This module includes classes and methods used for tests.

This is not meant to be used in general.
"""

from __future__ import annotations

from runtime_final import final


@final
class FinalClass:
    pass


class ClassWithFinals:
    @final
    def foo(self) -> None:
        pass

    @final
    def bar(self) -> None:
        pass

    @final
    @property
    def foo_property(self) -> None:
        return None

    @final
    @classmethod
    def foo_classmethod(cls) -> None:
        pass

    @final
    @staticmethod
    def foo_staticmethod() -> None:
        pass

    def foo_nofinal(self) -> None:
        pass

    def bar_nofinal(self) -> None:
        pass
