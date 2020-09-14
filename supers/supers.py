from typing import List, Optional, Any
from abc import ABCMeta


def get_method_owner(cls, method_name):
    if method_name in cls.__dict__:
        return cls
    else:
        for base in cls.__bases__:
            owner = get_method_owner(base, method_name)
            if owner:
                return owner
    return None


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
                    method = getattr(s, method_name)
                    method_owner = get_method_owner(s, method_name)
                    if method_owner and isinstance(
                        method_owner.__dict__[method_name], staticmethod
                    ):
                        r = method(*args, **kwargs)  # omit self
                    else:
                        r = method(self._owner, *args, **kwargs)  # pass on owner self
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

    Returns:
        object:
            object, which will broadcast methods called on it
            to all parent classes of owner.
            The results are subsequently returned in a list.
    """
    t = owner if type(owner) in [type, ABCMeta] else type(owner)
    return _Supers(owner=owner, superclasses=t.__bases__)
