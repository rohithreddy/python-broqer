"""
Emit every value delayed by the given time.

Usage:

>>> import asyncio
>>> from broqer import Subject, op
>>> s = Subject()
>>> s | op.delay(0.1) | op.sink(print)
<...>
>>> s.emit(1)
>>> s.emit(2)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.05))
>>> s.emit(3)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.07))
1
2
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.05))
3

"""
import asyncio
import sys
from typing import Any

from broqer import Publisher, default_error_handler

from .operator import Operator, build_operator


class Delay(Operator):
    def __init__(self, publisher: Publisher, duration: float,
                 error_callback=default_error_handler, loop=None) -> None:
        assert duration >= 0, 'delay has to be positive'

        Operator.__init__(self, publisher)

        self._duration = duration
        self._loop = loop or asyncio.get_event_loop()
        self._error_callback = error_callback

    def get(self):
        return Publisher.get(self)  # will raise ValueError

    def emit(self, value: Any, who: Publisher) -> None:
        assert who is self._publisher, 'emit from non assigned publisher'
        self._loop.call_later(self._duration, self._delayed, value)

    def _delayed(self, value):
        try:
            self.notify(value)
        except Exception:  # pylint: disable=broad-except
            self._error_callback(*sys.exc_info())


delay = build_operator(Delay)  # pylint: disable=invalid-name
