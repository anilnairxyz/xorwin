from arithmetic import Operation
from decimal import Decimal as D
from fractions import Fraction as F
from mixed_fractions import Mixed as M


def test_operation():
    operation = Operation("/", D(35), D(7))
    operation = Operation("+", operation, D(6))
    assert(operation.result == 11)
    operation = Operation("/", D(38.5), D(7))
    operation = Operation("+", operation, D(6.5))
    assert(operation.result == 12.0)
    operation = Operation("/", F(1, 3), F(1, 2))
    operation = Operation("+", operation, F(1, 3))
    assert(operation.result == 1)
    operation = Operation("/", D(38.5), D(7))
    operation = Operation("bracket", operation)
    operation = Operation("square", operation)
    operation = Operation("+", operation, D(6.5))
    assert(operation.result == 36.75)
    operation = Operation("/", F(1, 3), F(1, 2))
    operation = Operation("bracket", operation)
    operation = Operation("square", operation)
    operation = Operation("+", operation, F(1, 3))
    assert(operation.result == F(7, 9))
    operation = Operation("/", M(1, 1, 3), M(0, 1, 4))
    operation = Operation("+", operation, F(1, 3))
    assert(operation.result == M(5, 2, 3))
    operation = Operation("/", F(1, 3), F(1, 2))
    operation = Operation("bracket", operation)
    operation = Operation("square", operation)
    operation = Operation("+", operation, F(1, 3))
    assert(operation.result == F(7, 9))
