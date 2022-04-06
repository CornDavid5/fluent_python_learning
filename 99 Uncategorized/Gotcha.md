## mutable default argument
``` python
def append_to(element, to=[]):
    to.append(element)
    return to
```

Python’s default arguments are evaluated once when the function is defined, not each time the function is called.

``` python
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```

## late bind closures
``` python
def create_multipliers():
    return [lambda x : i * x for i in range(5)]

for multiplier in create_multipliers():
    print(multiplier(2))
    # all print 8
```

Python’s closures are late binding. This means that the values of variables used in closures are looked up at the time the inner function is called.

``` python
def create_multipliers():
    return [lambda x, i = i : i * x for i in range(5)]
    # this solution actual used the behavior that Python will evaluate the parameter when function is defined
```

## modifying list (add or delete element) while iterating over it
``` python
nums = [1, 2, 3, 5, 6, 7, 0, 1]
for ind, n in enumerate(nums):
    if n < 5:
        del(nums[ind])
# expected: nums = [5, 6, 7]
# actual:   nums = [2, 5, 6, 7, 1]
```

``` python
nums = [n for n in nums if n >= 5]
# or
nums[:] = [n for n in nums if n >= 5]
```

## chain comparison operators without parenthesis
``` python
print(5 > 2 == True) 
# expect False
# actual True
# 5 > 2 == True ==> 5 > 2 and 2 == True
``` 

## is, is not, ==, !=
``` python
print(1 == True)  # results is True
print(1 is True) # results is False
print(1 != False) # results is True 
print(1 is not False) # results is True
```

`is` and `==` are not the same thing, but `is not` and `!=` are same

## scope
``` python
list1 = [1, 2, 3]
def baz1():
  
    # the code works fine
    list1.append(4) 
    return list1

def baz2():
  
    # Doesn't work fine, because we are assigning 
    # to the variable list1 but list1 is not defined 
    # inside the scope of this function.
    list1 += [5]      
    return list1
```

## copy mutable value without using copy.copy() and copy.deepcopy()
``` python
spam = ['cat', 'dog', 'eel']
cheese = spam
spam[2] = 'MOOSE'
# cheese ['cat', 'dog', 'MOOSE']

bacon = [2, 4, 8, 16]
ham = copy.copy(bacon)
bacon[0] = 'CHANGED'
# bacon ['CHANGED', 4, 8, 16]
# ham [2, 4, 8, 16]

bacon = [[1, 2], [3, 4]]
ham = copy.copy(bacon)
bacon.append('APPENDED')
# bacon [[1, 2], [3, 4], 'APPENDED']
# ham [[1, 2], [3, 4]]
bacon[0][0] = 'CHANGED'
# bacon [['CHANGED', 2], [3, 4], 'APPENDED']
# ham [['CHANGED', 2], [3, 4]]

bacon = [[1, 2], [3, 4]]
ham = copy.deepcopy(bacon)
bacon[0][0] = 'CHANGED'
# bacon [['CHANGED', 2], [3, 4]]
# ham [[1, 2], [3, 4]]
```