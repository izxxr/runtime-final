# amulet-runtime-final
Declare final Python classes and methods at runtime.

This module provides a decorator based interface to declare final classes and methods that are enforced at runtime.
This module is inspired by and is compatible with [`typing.final`](https://docs.python.org/3/library/typing.html#typing.final).
See [PEP-591](https://www.python.org/dev/peps/pep-0591) for more details on this topic.

## Installation
**Python 3.6 or higher is required.**

You can simply install this module from `pip`.
```
python -m pip install amulet-runtime-final
```

## Usage
The main component of this module is the `final` decorator that
can be used to decorate classes and methods inside a class. As
such:

- Classes decorated with @final cannot be subclassed.
- Methods decorated with @final cannot be overriden in subclasses.

For example with classes:
```py
from runtime_final import final

@final
class Foo:
    ...

class Bar(Foo):  # Raises RuntimeError
    ...
```

And with methods:
```py
from runtime_final import final

class Foo:
    @final
    def foo(self):
        ...

class Bar(Foo):
    def foo(self):  # Raises RuntimeError
        ...
```

And with other decorators:
```py
from runtime_final import final

class Foo:
    @final
    @property
    def foo(self):
        ...
    
    @final
    @staticmethod
    def bar():
        ...
    
    @final
    @classmethod
    def baz(cls):
        ...

class Bar(Foo):
    @property
    def foo(self):  # Raises RuntimeError
        ...

    @staticmethod
    def bar():  # Raises RuntimeError
        ...
    
    @classmethod
    def baz(cls):  # Raises RuntimeError
        ...
```

With property setters:
```py
from runtime_final import final

class Foo:
    @property
    def foo(self):
        ...
    
    # Note that the `final` decorator must only be applied to the last definition.
    
    @final
    @foo.setter
    def foo(self, foo):
        ...
```
