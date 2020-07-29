# Supers: Call a function in all superclasses as easy as `supers(self).foo(42)`

![Python package](https://github.com/LukasHedegaard/supers/workflows/Python%20package/badge.svg) 
[![codecov](https://codecov.io/gh/LukasHedegaard/supers/branch/master/graph/badge.svg)](https://codecov.io/gh/LukasHedegaard/datasetops) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation
```bash
pip install supers
```

### Development installation
```bash
pip install -e .[tests,build]
```

## Example
Say you have a class inheriting from multiple parent classes, and you would like a function for each parent. With `supers` this becomes as easy as:

```python
from supers import supers

class Parent1:
    def __init__(self, m:float):
        self.m1 = m * 1

    def mult(self, value):
        return value * self.m1

class Parent2:
    def __init__(self, m:float):
        self.m2 = m * 2

    def mult(self, value):
        return value * self.m2

class Child(Parent1, Parent2):
    def __init__(self, m):
        supers(self).__init__(m)

    def allmult(self, val):
        return supers(self).mult(val)

c = Child(m=10)

# Parent attributes were updated
assert c.m1 == 10 
assert c.m2 == 20

# Parent1.mult is called as expected
assert c.mult(10) == 100

# Each parent is called and results are returned in a list
assert c.allmult(10) == supers(c).mult(10) == [100, 200]

```
