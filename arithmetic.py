import operator as op
from random import choice, randint
from decimal import Decimal as D
import json


class Operation:

    opcodes = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv}

    def __init__(self, operation="+", operand=(0, 0)):

        self.sequence = None
        self.result = None
        previous_results = []

        if operation in ("+", "-", "*", "/"):
            self.sequence = {"operation": operation, "operand": []}
            if isinstance(operand[0], Operation):
                self.sequence["operand"].append(operand[0].sequence)
                previous_results.append(operand[0].result)
            else:
                self.sequence["operand"].append(operand[0])
                previous_results.append(operand[0])

            if isinstance(operand[1], Operation):
                self.sequence["operand"].append(operand[1].sequence)
                previous_results.append(operand[1].result)
            else:
                self.sequence["operand"].append(operand[1])
                previous_results.append(operand[1])

            self.result = self.opcodes[operation](*previous_results)

        elif operation == "square":
            self.sequence = {"operation": operation, "operand": []}
            if isinstance(operand, Operation):
                self.sequence["operand"].append(operand.sequence)
                self.result = operand.result ** 2
            else:
                self.sequence["operand"].append(operand)
                self.result = operand ** 2

        elif operation == "bracket":
            self.sequence = {"operation": operation, "operand": []}
            if isinstance(operand, Operation):
                self.sequence["operand"].append(operand.sequence)
                self.result = operand.result
            else:
                raise ValueError("Bracket can only be performed only over another Operation")

        else:
            raise ValueError("Unsupported Operation")

        parsed = json.loads(self.sequence)
        print(json.dumps(parsed, indent=4, sort_keys=True))


class Question1:

    def __init__(self):
        self.allowed_operations = ["/", "*", "+", "-"]
        self.operand_count = 4
        self.range = (1, 100)

        operand_seq = [None]*self.operand_count
        operation_seq = []
        for i in range(0, self.operand_count-1):
            operation_seq.append(choice(self.allowed_operations))

        for i, y in enumerate(operation_seq):
            if y == "/":
                if not operand_seq[i]:
                    operand_seq[i+1], operand_seq[i] = self._create_division()
                else:
                    operand_seq[i+1], _ = self._create_division(divisor=operand_seq[i])

        for i, y in enumerate(operation_seq):
            if y == "*":
                if not (operand_seq[i] or operand_seq[i+1]):
                    operand_seq[i], operand_seq[i+1] = self._create_multiplication()
                elif not operand_seq[i]:
                    operand_seq[i], _ = self._create_multiplication()
                elif not operand_seq[i+1]:
                    operand_seq[i+1], _ = self._create_multiplication()

        for i, y in enumerate(operation_seq):
            if y in ("+", "-"):
                if not (operand_seq[i] or operand_seq[i+1]):
                    operand_seq[i], operand_seq[i+1] = self._create_addition()
                elif not operand_seq[i]:
                    operand_seq[i], _ = self._create_addition()
                elif not operand_seq[i+1]:
                    operand_seq[i+1], _ = self._create_addition()

        print(operand_seq)
        print(operation_seq)

    def _create_division(self, divisor=None):
        if not divisor:
            divisor = randint(self.range[0], D(self.range[1]).sqrt())
        quotient = randint(self.range[0], D(self.range[1]).sqrt())
        dividend = quotient * divisor
        return dividend, divisor

    def _create_multiplication(self):
        a = randint(self.range[0], D(self.range[1]).sqrt())
        b = randint(self.range[0], D(self.range[1]).sqrt())
        return a, b

    def _create_addition(self):
        a = randint(*self.range)
        b = randint(*self.range)
        return a, b


if __name__ == "__main__":
    q = Question1()
