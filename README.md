# runtime-final
Declare final Python classes and methods at runtime.

## Overview
This module provides a decorator interface to declare final
classes and methods.

This module is inspired by and is compatible with `typing.final`.
See [PEP-591](https://www.python.org/dev/peps/pep-0591) for more
details on this topic.

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

## Compatibility with `typing.final`
This module is also compatible with the `final` decorator
provided by the typing module from standard library. You
can easily combine this module with typing module.

```py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import final
else:
    from runtime_final import final
```
> `typing.TYPE_CHECKING` is always False at runtime while is True for type checkers.

## Documentation
For more details, see the [documentation](https://github.com/nerdguyahmad/runtime-final/wiki)
