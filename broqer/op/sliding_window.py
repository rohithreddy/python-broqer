"""
Group ``size`` emitted values overlapping

Usage:

>>> from broqer import Subject, op
>>> s = Subject()

>>> window_publisher = s | op.sliding_window(3)
>>> _d = window_publisher | op.sink(print, 'Sliding Window:')
>>> s.emit(1)
>>> s.emit(2)
>>> s.emit(3)
Sliding Window: (1, 2, 3)
>>> with window_publisher | op.sink(print, '2nd subscriber:'):
...     pass
2nd subscriber: (1, 2, 3)
>>> s.emit((4, 5))
Sliding Window: (2, 3, (4, 5))
>>> window_publisher.flush()
>>> s.emit(5)
>>> _d.dispose()
"""
import asyncio
from collections import deque
from typing import Any, MutableSequence  # noqa: F401

from broqer import Publisher, Subscriber

from .operator import Operator, build_operator


class SlidingWindow(Operator):
    def __init__(self, publisher: Publisher, size: int,
                 emit_partial=False) -> None:
        assert size > 0, 'size has to be positive'

        Operator.__init__(self, publisher)

        self._state = deque(maxlen=size)  # type: MutableSequence
        self._emit_partial = emit_partial

    def unsubscribe(self, subscriber: Subscriber) -> None:
        Operator.unsubscribe(self, subscriber)
        if not self._subscriptions:
            self._state.clear()

    def get(self):
        if not self._subscriptions:
            if self._emit_partial or self._state.maxlen == 1:
                return (self._publisher.get(),)  # may raises ValueError
        if self._emit_partial or \
                len(self._state) == self._state.maxlen:  # type: ignore
            if self._state:
                return tuple(self._state)
        return Publisher.get(self)  # raises ValueError

    def emit(self, value: Any, who: Publisher) -> asyncio.Future:
        assert who is self._publisher, 'emit from non assigned publisher'
        self._state.append(value)
        if self._emit_partial or \
                len(self._state) == self._state.maxlen:  # type: ignore
            return self.notify(tuple(self._state))
        return None

    def flush(self):
        self._state.clear()


sliding_window = build_operator(SlidingWindow)  # pylint: disable=invalid-name
