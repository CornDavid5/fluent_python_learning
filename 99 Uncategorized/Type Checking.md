# Type Checking
Python is a dynamically typed language. This means that the Python interpreter does type checking only as code runs, and that the type of a variable is allowed to change over its lifetime. 

## Type Hints and Type Annotations
Type hints by thmeselves don't cause Python to enforce types. Type hints can be acheived by using type annotation or type comment

``` python
def headline(text: str, align: bool = True) -> str:
    prefix: str = '-'
    ...
```

``` python
from typing import Dict, List, Tuple

names: List[str] = ['Guido', 'Jukka', 'Ivan']
version: Tuple[int, int, int] = (3, 7, 1)
optoins: Dict[str, bool] = {'centered': False, 'capitalize': True}
```

- when you run the program, you can inspect the annotation associated with a function using `.__annotation__` attribute on the function

    ``` python
    from typing import List, Sequence

    def square(elems: Sequence[float]) -> List[float]:
        return [x ** 2 for e in elems]
    ```
- `Any` type is a special type. It makes `Gradual Typing` possible.
- `Union` and `Optional` type
    ``` python
    # before 3.10
    from typing import Optional, Union
    def f(param: Optional[int]) -> Union[float, str]:
        ...
    
    # after 3.10
    def f(param: int | None) -> float | str:
        ...

    ```
    - `Optional[X]` is equivalent to `X | None` (or `Union[X, None]`)
    - An optional argument with a default does not require the Optional qualifier on its type annotation just because it is optional.
- annotating *args and **kwargs, you should only annotate the type of each element, not the sequence. For example, you should use `str` and not `Tuple[str]`.

## Type Aliases
``` python
Vector = list[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]
```

## Generics
- when the function only expects to receive a sequence of data, doesn't care if it is list or tuple, you can use `Sequence`. Sequence is an object which supports `__len__`,`__getitem__`
- another common type, Mapping is an object which defines the `__getitem__`,`__len__`,`__iter__`
- generics can be parameterized by using a factory function available in typing called `TypeVar`, it exist primarily for the benefit of static type checkers.

    ``` python 
    from typing import Sequence, TypeVar

    Choosable = TypeVar("Choosable", str, float) # define type variable, and limit it to be either str or float

    def choose(items: Sequence[Choosable]) -> Choosable:
        return random.choice(items)

    reveal_type(choose(["Guido", "Jukka", "Ivan"])) # 'builtins.str*'
    reveal_type(choose([1, 2, 3]))                  # 'builtins.float*'
    reveal_type(choose([True, 42, 3.14]))           # 'builtins.float*'
    reveal_type(choose(["Python", 3, 7]))           # error: expected 'str' or 'float', got 'object'
    ```

## Subtypes
- a type T is a subtype of U if the following two conditions hold:
    - Every value from T is also in the set of values of U type.
    - Every function from U type is also in the set of functions of T type.
- The importance of subtypes is that a subtype can always pretend to be its supertype.

## Consistent Type
- The type T is consistent with the type U if T is a subtype of U or either T or U is Any.