from typing import Any, Callable

from broqer import Publisher

from ._operator import Operator, build_operator


class Map(Operator):
  def __init__(self, publisher:Publisher, map_func:Callable[[Any], Any]):
    """ special care for return values:
        * return `None` (or nothing) if you don't want to return a result
        * return `None,` if you want to return `None`
        * return `(a,b),` to return a tuple as value
        * every other return value will be unpacked
    """
 
    Operator.__init__(self, publisher)

    self._map_func=map_func

  def emit(self, *args:Any, who:Publisher) -> None:
    *args,_=self._map_func(*args),None
    try:
        *args,=args[0]
    except TypeError:
        if args[0] is None:
            args=()
    self._emit(*args)

map=build_operator(Map)