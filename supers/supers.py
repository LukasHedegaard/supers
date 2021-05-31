from typing import List, Optional, Any
from abc import ABCMeta
import inspect


def get_method_owner(cls, method_name):
    if method_name in cls.__dict__:
        return cls
    else:
        for base in cls.__bases__:
            owner = get_method_owner(base, method_name)
            if owner:
                return owner
    return None  # pragma: no cover


def args_match(method, args: list, kwargs: dict, include_self=False):
    num_given = len(args) + len(kwargs)
    parameters = inspect.signature(method).parameters
    num_needed = len(
        [True for v in parameters.values() if v.default is inspect.Parameter.empty]
    ) - int(include_self)
    num_givable = len(parameters) - int(include_self)
    return num_given <= num_givable and num_given >= num_needed


class _Supers:
    def __init__(self, *args, **kwargs):
        """ To initialize, use _Supers(owner=self, superclasses=superclasses)
            Otherwise, __init__ of the other superclasses is called
        """
        if "owner" in kwargs and "superclasses" in kwargs:
            self._superclasses: List = kwargs["superclasses"]
            self._owner = kwargs["owner"]
        else:
            self.__getattr__("__init__")(*args, **kwargs)

    def __getattr__(self, method_name: str):
        def wrapper(*args, **kwargs) -> Optional[List[Any]]:
            results = []
            for s in self._superclasses:
                if hasattr(s, method_name):
                    r = None
                    method = getattr(s, method_name)
                    method_owner = get_method_owner(s, method_name)
                    if method_owner and isinstance(
                        method_owner.__dict__[method_name], staticmethod
                    ):  # omit self
                        if args_match(method, args, kwargs):
                            r = method(*args, **kwargs)
                    else:  # pass on owner self
                        if args_match(method, args, kwargs, include_self=True):
                            r = method(self._owner, *args, **kwargs)
                    if r is not None:
                        results.append(r)

            return results

        return wrapper

    def __getitem__(self, i) -> "_Supers":
        if type(i) == int:
            new_superclasses = [self._superclasses[i]]
        elif type(i) == slice:
            new_superclasses = self._superclasses[i]
        else:
            raise IndexError("Index of type {} is not supported".format(type(i)))

        return _Supers(owner=self._owner, superclasses=new_superclasses)


def supers(owner):
    """ Returns an object, which will broadcast methods called on it
        to all parent classes of owner.
        The results are subsequently returned in a list.

    Args:
        owner (object): A childclass with at least one parent
        strict (bool): Whether argument count should match exactly

    Returns:
        object:
            object, which will broadcast methods called on it
            to all parent classes of owner.
            The results are subsequently returned in a list.
    """
    t = owner if type(owner) in [type, ABCMeta] else type(owner)
    return _Supers(owner=owner, superclasses=t.__bases__)
