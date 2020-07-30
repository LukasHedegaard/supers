from typing import List, Optional, Any


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

    def __getattr__(self, called_method: str):
        def wrapper(*args, **kwargs) -> Optional[List[Any]]:
            results = []
            for s in self._superclasses:
                if hasattr(s, called_method):
                    method = getattr(s, called_method)
                    if isinstance(s.__dict__[called_method], staticmethod):
                        r = method(*args, **kwargs)  # omit self
                    else:
                        r = method(self._owner, *args, **kwargs)  # pass on owner self
                    if r is not None:
                        results.append(r)

            return results

        return wrapper


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
    t = owner if type(owner) == type else type(owner)
    superclasses = t.mro()[1:-1]
    return _Supers(owner=owner, superclasses=superclasses)
