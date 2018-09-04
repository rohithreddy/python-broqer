import pytest

from broqer.op import All
from broqer import StatefulPublisher, NONE

from .helper import check_single_operator, check_multi_operator

@pytest.mark.parametrize('args, kwargs, input_vector, output_vector', [
    ((), {}, (False, False, True, False), (False, NONE, True, False)),
    ((), {'predicate':lambda v:v}, (False, False, True, False), (False, NONE, True, False)),
    ((), {'predicate':lambda v:v>0}, (0, -1, 1, 2, 0), (False, NONE, True, NONE, False)),
    ((StatefulPublisher(True),), {}, (False, False, True, False), (False, NONE, True, False)),
    ((StatefulPublisher(True),), {'predicate':lambda v:v}, (False, False, True, False), (False, NONE, True, False)),
    ((StatefulPublisher(1),), {'predicate':lambda v:v>0}, (0, -1, 1, 2, 0), (False, NONE, True, NONE, False)),
    ((StatefulPublisher(False),), {}, (False, False, True, False), (False, NONE, NONE, NONE)),
    ((StatefulPublisher(False),), {'predicate':lambda v:v}, (False, False, True, False), (False, NONE, NONE, NONE)),
    ((StatefulPublisher(-1),), {'predicate':lambda v:v>0}, (0, -1, 1, 2, 0), (False, NONE, NONE, NONE, NONE)),
])
def test_with_publisher(args, kwargs, input_vector, output_vector):
    check_single_operator(All, args, kwargs, input_vector, output_vector, has_state=True)

@pytest.mark.parametrize('kwargs, input_vector, output_vector', [
    ({}, ((False,), (False,), (True,), (False,)), (False, NONE, True, False)),
    ({}, ((False, False), (NONE, False), (NONE, True), (True, NONE), (False, NONE), (NONE, False)), (False, NONE, NONE, True, False, NONE)),
])
def test_with_publishers(kwargs, input_vector, output_vector):
    check_multi_operator(All, kwargs, input_vector, output_vector, has_state=True)