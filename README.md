# runtime-final
Declare final Python classes and methods at runtime.

This module provides a decorator based interface to declare final
classes and methods. This module is inspired by and is compatible with [`typing.final`](https://docs.python.org/3/library/typing.html#typing.final).
See [PEP-591](https://www.python.org/dev/peps/pep-0591) for more
details on this topic.

## Installation
**Python 3.6 or higher is required.**

You can simply install this module from `pip`.
```
python -m pip install runtime-final
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

class User:
    @final
    def edit(self):
        ...

class AnotherUser(User):
    def edit(self):  # Raises RuntimeError
        ...
```

## Documentation
For more details, see the [documentation](https://runtime-final.readthedocs.io)
