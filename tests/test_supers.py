from abc import ABC, abstractmethod
from supers import supers
import pytest


def test_basics():
    class Parent1:
        def __init__(self, m: float):
            self.m1 = m * 1

        def mult(self, value):
            return value * self.m1

    class Parent2:
        def __init__(self, m: float):
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

    with pytest.raises(AttributeError):
        c.dummy()  # type: ignore


def test_static_methods():
    class Abstract(ABC):
        @staticmethod
        @abstractmethod
        def value():
            ...

        @staticmethod
        def inherited_static():
            return 42

    class Parent1(Abstract):
        @staticmethod
        def value():
            return 1

        def other(self):
            return 0

    class Parent2(Abstract):
        @staticmethod
        def value():
            return 2

    class Child(Parent1, Parent2):
        @staticmethod
        def values():
            return supers(Child).value()

    c = Child()

    # Parent1.value is called as expected
    assert c.value() == 1

    assert c.other() == 0

    # Each parent is called and results are returned in a list
    assert c.values() == Child.values() == [1, 2]

    assert supers(Child).inherited_static() == [42, 42]


def test_slicing():
    class Parent1:
        def value(self):
            return 1

    class Parent2:
        def value(self):
            return 2

    class Parent3:
        def value(self):
            return 3

    class Child(Parent1, Parent2, Parent3):
        def values(self):
            return supers(Child).value()

    c = Child()

    # Single
    assert supers(c)[1].value() == [2]

    # Slice
    assert supers(c)[1:].value() == [2, 3]

    # Error scenario
    with pytest.raises(IndexError):
        supers(c)["1"]


def test_only_call_if_sufficient_args_given():
    class Parent1:
        def __init__(self, m: float = 42):
            self.m1 = m * 1

    class Parent2:  # Not called: Lacks args
        def __init__(self, m: float, n: float):
            self.m2 = m * n

    class Parent3:  # Not called: Too many args
        def __init__(self):
            self.m3 = 42

    class Parent4:  # Called, has default args
        def __init__(self, m: float, n: float = 2):
            self.m4 = m * n

    class Child(Parent1, Parent2, Parent3, Parent4):
        def __init__(self, m):
            supers(self).__init__(m)

    c = Child(m=10)

    # Parent attributes were updated
    assert c.m1 == 10
    assert not hasattr(c, "m2")
    assert not hasattr(c, "m3")
    assert c.m4 == 20
