# Dictionaries and Sets

## Dictionary
### Dict Syntax
- dictionary comprehension
    - A dictcomp builds a dict instance by taking key:value pairs from any iterable.
    - {key:value for item in iterable if condition == True}
- Unpacking dict
    - we can apply `**` to more than one argument in a function call. All keys are unique.
        ``` python
        >>> def dump(**kwargs):
        ...     return kwargs
        ...
        >>> dump(**{'x': 1}, y=2, **{'z': 3})
        {'x': 1, 'y': 2, 'z': 3}
        ```
    - we can apply `**` inside a dict literal. Keys can be duplicate and later ones will overwrite previous ones.
        ``` python
        >>> {'a': 0, **{'x': 1}, 'y': 2, **{'z': 3, 'x': 4}}
        {'a': 0, 'x': 4, 'y': 2, 'z': 3}
        ```
- Merge dicts
    - `|` and `|=` can be used to merge dicts. `|` create a new mapping, `|=` update an existing mapping in-place. Alternative is to use `update` method.
- Pattern Matching with Mapping
    ``` python
    def get_creators(record: dict) -> list:
    match record:
        # 'authors' key mapped to a sequence. Return the items in the sequence, as a new list
        case {'type': 'book', 'api': 2, 'authors': [*names]}:  
            return names
        # 'author' key mapped to any object. Return the object inside a list.
        case {'type': 'book', 'api': 1, 'author': name}:  
            return [name]
        # Any other mapping with 'type': 'book' is invalid, raise ValueError.
        case {'type': 'book'}:  
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:  
            return [name]
        case _:  
            raise ValueError(f'Invalid record: {record!r}')
    ```
    - one difference when comparing to sequence matching is that dict matching can do partial matches. For example, a dict {'type': 'book', 'api': 1, 'author': 'test', 'title': 'new me'} will still match the second case, even though title is not specified in the second case. 
    - The automatic handling of missing keys is not triggered because pattern matching always uses the d.get(key, sentinel) method — where the default sentinel is a special marker value that cannot occur in user data.
- Overview of Common Mapping Methods
    - setdefault(key, default_value)

### Inconsistent usage of __missing__ in the standard library 
- The default_factory of a `defaultdict` is only invoked to provide default values for `__getitem__` calls, and not for the other methods. For example, if `dd` is a `defaultdict`, and k is a missing key, `dd[k]` will call the default_factory to create a default value, but `dd.get(k)` still returns None, and `k in dd` is False.
- A subclass of `dict` implementing only `__missing__` and no other method. In this case, `__missing__` may be called only on `d[k]`, which will use the `__getitem__` inherited from dict.
- A subclass of `collections.UserDict` implementing only `__missing__` and no other method. The `get` method inherited from UserDict calls `__getitem__`. This means `__missing__` may be called to handle lookups with `d[k]` and `d.get(k)`.
- A minimal subclass of `abc.Mapping` implementing `__missing__` and the required abstract methods, including an implementation of `__getitem__` that calls `__missing__`. The `__missing__` method is triggered in this class for missing key lookups made with `d[k]`, `d.get(k)`, and `k in d`.

### Immutable Mapping
- using wrapper class called `MappingProxyType` from `types` module.

### Dictionary views
- `.keys()`, `.values()`, `.items()` all return a view.

## Set
### Set Overview 
- `set` is not ordered. If you want to perserve the first occurence of each item, you can use `dict` to achieve that: `list(dict.fromkeys(l).keys())`
- each element is `set` must be hashable, but `set` type is not hashable. `frozenset` type is hashable.
- set comprehension: {expression for item in iterable if condition == True}
- membership test is very efficient

