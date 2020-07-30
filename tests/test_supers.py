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
    class Parent1:
        @staticmethod
        def value():
            return 1

        def other(self):
            return 0

    class Parent2:
        @staticmethod
        def value():
            return 2

    class Child(Parent1, Parent2):
        @staticmethod
        def values():
            return supers(Child).value()

    c = Child()

    # Parent1.mult is called as expected
    assert c.value() == 1

    # Each parent is called and results are returned in a list
    assert c.values() == Child.values() == [1, 2]
