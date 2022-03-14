# An Array of Sequences

## Overview of Built-in Sequences
- Container sequences
    - Can hold items of different types, including nested containers. Some examples: `list`, `tuple`, and `collections.deque`.
    - A container sequence holds references to the objects it contains, which may be of any type

- Flat sequences
    - Hold items of one simple atomic types like integers, floats, or characters. Some examples: `str`, `bytes`, and `array.array`.
    - A flat sequence stores the value of its contents in its own memory space, and not as distinct Python objects

- Mutable sequences
    - E.g. `list`, `bytearray`, `array.array`, and `collections.deque`.

- Immutable sequences
    - E.g. `tuple`, `str`, and `bytes`.

## List Comprehension and Generator Expression
- listcomps vs genexps
    - listcomps use to create list, while genexps use to create sequence
    - genexp saves memory because it yields items one by one using the iterator protocol instead of building a whole list just to feed another constructor.
- Local Scope and Walrus operator `:=`
    ``` python
    >>> x = 'ABC'
    >>> codes = [ord(x) for x in x]
    >>> x  
    'ABC'
    >>> codes
    [65, 66, 67]
    >>> codes = [last := ord(c) for c in x]
    >>> last  
    67
    >>> c  
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    NameError: name 'c' is not defined
    ```

- [expression for item in iterable if condition == True]
- (expression for item in iterable if condition == True)

## Tuple
- Tuple as records
    ``` python
    lax_coordinates = (33.9425, -118.408056)  
    city, year, pop, chg, area = ('Tokyo', 2003, 32_450, 0.66, 8014)  
    traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
    ```
- Tuple as immutable list
    ``` python 
    >>> a = (10, 'alpha', [1, 2])
    >>> b = (10, 'alpha', [1, 2])
    >>> a == b
    True
    >>> b[-1].append(99)
    >>> a == b
    False
    >>> b
    (10, 'alpha', [1, 2, 99])
    ```
    - a tuple with mutable element is not hashable
- single-item tuples must be written with trailing comma. (record,)

## Unpacking Sequences and Iterables
- Unpacking works with any iterable object as the data source—including iterators which don’t support index notation []. The only requirement is that the iterable yields exactly one item per variable in the receiving end, unless you use a star (*) to capture excess items.

``` python
# simple unpacking
lax_coordinates = (33.9425, -118.408056)
latitude, longitude = lax_coordinates

# use * to grab excess items
a, b, *rest = range(5) # (0, 1, [2, 3, 4])
a, b, *rest = range(3) # (0, 1, [2])
a, b, *rest = range(2) # (0, 1, [])

# unpack with * in function call and sequence literal
def fun(a, b, c, d, *rest):
    return a, b, c, d, rest
fun(*[1, 2], 3, *range(4, 7)) # (1, 2, 3, 4, (5, 6))

{*range(4), 4, *(5, 6, 7)} # {0, 1, 2, 3, 4, 5, 6, 7}
```

## Pattern Matching with Sequences
``` python
def handle_command(self, message):
    match message: 
        case ['BEEPER', frequency, times]: 
            self.beep(times, frequency)
        case ['NECK', angle]: 
            self.rotate_neck(angle)
        case ['LED', ident, intensity]: 
            self.leds[ident].set_brightness(ident, intensity)
        case ['LED', ident, red, green, blue]: 
            self.leds[ident].set_color(ident, red, green, blue)
        case _: 
            raise InvalidCommand(message)

# deconstructuring
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

for record in metro_areas:
    match record:
        case [name, _, _, (float(lat), float(lon)) as coord] if lon <= 0:
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

# you can also match a instance of a class. Alternative way is using if block with isinstance function
def evaluate(exp: Expression, env: Environment) -> Any:
    "Evaluate an expression in an environment."
    match exp:
    # ... lines omitted
        # (quote exp)
        case ['quote', x]: 
            return x
        # (if test conseq alt)
        case ['if', test, consequence, alternative]: 
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)
        # (lambda (parms…) body1 body2…)
        case ['lambda', [*parms], *body] if body:  
            return Procedure(parms, body, env)
        # (define name exp)
        case ['define', Symbol() as name, value_exp]: 
            env[name] = evaluate(value_exp, env)
        # (define (name parm…) body1 body2…)
        case ['define', [Symbol() as name, *parms], *body] if body: 
            env[name] = Procedure(parms, body, env)
        # ... more lines omitted
        case _: 
            raise SyntaxError(lispstr(exp))
```
- Instances of `str`, `bytes`, and `bytearray` are not handled as sequences in the context of match/case. A `match` subject of one of those types is treated as an “atomic” value—like the integer 987 is treated as one value, not a sequence of digits. 

## Slicing
- To evaluate the expression `seq[start:stop:step]`, Python calls `seq.__getitem__(slice(start, stop, step))`
- Name a slice
``` python
>>> invoice = """
... 0.....6.................................40........52...55........
... 1909  Pimoroni PiBrella                     $17.50    3    $52.50
... 1489  6mm Tactile Switch x20                 $4.95    2     $9.90
... 1510  Panavise Jr. - PV-201                 $28.00    1    $28.00
... 1601  PiTFT Mini Kit 320x240                $34.95    1    $34.95
... """
>>> SKU = slice(0, 6)
>>> DESCRIPTION = slice(6, 40)
>>> UNIT_PRICE = slice(40, 52)
>>> QUANTITY =  slice(52, 55)
>>> ITEM_TOTAL = slice(55, None)
>>> line_items = invoice.split('\n')[2:]
>>> for item in line_items:
...     print(item[UNIT_PRICE], item[DESCRIPTION])
$17.50   Pimoroni PiBrella
$4.95   6mm Tactile Switch x20
$28.00   Panavise Jr. - PV-201
$34.95   PiTFT Mini Kit 320x240
```
- Assign to slice
``` python
>>> l = list(range(10))
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l[6:8] = [6,7,8]
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9]
>>> del l[2:4]
>>> l
[0, 1, 4, 5, 6, 7, 8, 8, 9]
```
- List of lists
``` python
>>> board = [['_'] * 3 for i in range(3)] 
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[1][2] = 'X' 
>>> board
[['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]

# be aware of list of mutable object
>>> weird_board = [['_'] * 3] * 3 
>>> weird_board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> weird_board[1][2] = 'O'
>>> weird_board
[['_', '_', 'O'], ['_', '_', 'O'], ['_', '_', 'O']]
```
- Augmented Assignment with Sequences
- The augmented assignment operators += and *= behave quite differently depending on the first operand. The special method that makes `+=` work is `__iadd__` (for “in-place addition”). However, if `__iadd__` is not implemented, Python falls back to calling `__add__`.
``` python
>>> l = [1, 2, 3]
>>> id(l)
4311953800 
>>> l *= 2
>>> l
[1, 2, 3, 1, 2, 3]
>>> id(l)
4311953800 
>>> t = (1, 2, 3)
>>> id(t)
4312681568 
>>> t *= 2
>>> id(t)
4301348296
```

## Alternative to List
- Arrays
    - use less memory comparing to list. For example, an array of float values does not hold full-fledged float instances, but only the packed bytes representing their machine values
    - the `array` type does not have an in-place sort method like `list.sort()`. If you need to sort an array, use the built-in sorted function to rebuild the array: `a = array.array(a.typecode, sorted(a))`
    - To keep a sorted array sorted while adding items to it, use the `bisect.insort` function
    - common type code:
        - 'b' signed char, 'B' unsigned char, 'h' signed short, 'H' unsigned short, 'i' signed int, 'I' unsigned int, 'l' signed long,  'L' unsigned long int, 'f' float, 'd' double
- Memory View
    - shared-memory sequence type that lets you handle slices of arrays without copying bytes.
    ``` python
    >>> from array import array
    >>> octets = array('B', range(6)) 
    >>> m1 = memoryview(octets)
    >>> m1.tolist()
    [0, 1, 2, 3, 4, 5]
    >>> m2 = m1.cast('B', [2, 3])
    >>> m2.tolist()
    [[0, 1, 2], [3, 4, 5]]
    >>> m3 = m1.cast('B', [3, 2])
    >>> m3.tolist()
    [[0, 1], [2, 3], [4, 5]]
    >>> m2[1,1] = 22
    >>> m3[1,1] = 33
    >>> octets
    array('B', [0, 1, 2, 33, 22, 5])

    >>> numbers = array.array('h', [-2, -1, 0, 1, 2])
    >>> memv = memoryview(numbers) 
    >>> len(memv)
    5
    >>> memv[0] 
    -2
    >>> memv_oct = memv.cast('B') 
    >>> memv_oct.tolist() 
    [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
    >>> memv_oct[5] = 4 
    >>> numbers
    array('h', [-2, -1, 1024, 1, 2]) 
    ```
- Other
    - collections.deque
        - appendleft, append, popleft, pop, extendleft, extend, remove, reverse, rotate, count, 
    - heapq
        - heappush, heappop, heapify