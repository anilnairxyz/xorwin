from random import sample, randint
from decimal import Decimal
from fractions import Fraction
from mixed_fractions import Mixed
from clint.textui import colored, puts, prompt


class Operation:
    """An operation format class.
    """

    def __init__(self, operation="+", *operands):

        self.sequence_json = {"operation": operation, "operand": []}
        self.sequence_str = []
        self.formula = []
        self.result = None
        self.operand_str = {"+": " + ", "-": " - ", "*": " * ", "/": " \u00F7 ", "square": " **2 "}
        self.operand_for = {"+": " + ", "-": " - ", "*": " * ", "/": " / ", "square": " **2 "}

        if operation in ("+", "-", "*", "/", "square"):
            for i, operand in enumerate(operands):
                if isinstance(operand, Operation):
                    self.sequence_json["operand"].append(operand.sequence_json)
                    self.formula.append(operand.formula)
                    self.sequence_str.append(operand.sequence_str)
                else:
                    self.sequence_json["operand"].append(operand)
                    self.formula.append(repr(operand))
                    self.sequence_str.append(str(operand))
                if i < len(operands)-1 or operation == "square":
                    self.formula.append(f" {self.operand_for[operation]} ")
                    self.sequence_str.append(f" {self.operand_str[operation]} ")

        elif operation == "bracket":
            if isinstance(operands[0], Operation):
                self.sequence_json["operand"].append(operands[0].sequence_json)
                self.formula.append(" (")
                self.formula.append(operands[0].formula)
                self.formula.append(") ")
                self.sequence_str.append(" (")
                self.sequence_str.append(operands[0].sequence_str)
                self.sequence_str.append(") ")
            else:
                raise ValueError("Bracket can only be performed over another Operation")

        else:
            raise ValueError("Unsupported Operation")

        self.formula = "".join(x for x in self.formula)
        self.sequence_str = "".join(x for x in self.sequence_str)
        self.result = eval(self.formula)


class Question1:
    """Framing BODMAS questions of the type a * b + c / d

    """

    def __init__(self, operations=["/", "*", "+", "-"], operand_count=4, value_range=(1, 100)):
        self.operations = operations
        self.operand_count = operand_count
        self.value_range = value_range
        self._operation_count = self.operand_count - 1
        self._sample_operations = self.operations * (max(len(self.operations), 2) * 2)
        self.operand_seq = None
        self.operation_seq = None
        self.question = None

    @property
    def operations(self):
        return self.__operations

    @operations.setter
    def operations(self, operations):
        self.__operations = operations
        self._sample_operations = self.operations * (max(len(self.operations), 2) * 2)

    @property
    def operand_count(self):
        return self.__operand_count

    @operand_count.setter
    def operand_count(self, operand_count):
        self.__operand_count = operand_count
        self._operation_count = self.operand_count - 1

    def frame_integer_question(self):
        self.operand_seq = [None] * self.operand_count
        self.operation_seq = sample(self._sample_operations, self._operation_count)
        dividend_seq = [1]*self._operation_count
        for i, y in enumerate(self.operation_seq):
            if y == "/":
                if not self.operand_seq[i]:
                    self.operand_seq[i+1], self.operand_seq[i] = self._create_integer_division()
                    dividend_seq[i] = self.operand_seq[i+1] * self.operand_seq[i]
                else:
                    self.operand_seq[i+1], _ = self._create_integer_division(divisor=dividend_seq[i-1])
                    dividend_seq[i] = dividend_seq[i-1] * self.operand_seq[i+1]

        for i, y in enumerate(self.operation_seq):
            if y == "*":
                if not (self.operand_seq[i] or self.operand_seq[i+1]):
                    self.operand_seq[i], self.operand_seq[i+1] = self._create_integer_multiplication()
                elif not self.operand_seq[i]:
                    self.operand_seq[i], _ = self._create_integer_multiplication()
                elif not self.operand_seq[i+1]:
                    self.operand_seq[i+1], _ = self._create_integer_multiplication()

        for i, y in enumerate(self.operation_seq):
            if y in ("+", "-"):
                if not (self.operand_seq[i] or self.operand_seq[i+1]):
                    self.operand_seq[i], self.operand_seq[i+1] = self._create_integer_addition()
                elif not self.operand_seq[i]:
                    self.operand_seq[i], _ = self._create_integer_addition()
                elif not self.operand_seq[i+1]:
                    self.operand_seq[i+1], _ = self._create_integer_addition()

        self.operand_seq.reverse()
        self.operation_seq.reverse()
        self.question = self._combine_operations()
        return self.question

    def _create_integer_division(self, divisor=None):
        div_range = (int(Decimal(self.value_range[0]).sqrt()), int(Decimal(self.value_range[1]).sqrt()))
        if not divisor:
            divisor = randint(*div_range)
        quotient = randint(*div_range)
        dividend = quotient * divisor
        return dividend, divisor

    def _create_integer_multiplication(self):
        mul_range = (int(Decimal(self.value_range[0]).sqrt()), int(Decimal(self.value_range[1]).sqrt()))
        a = randint(*mul_range)
        b = randint(*mul_range)
        return a, b

    def _create_integer_addition(self):
        a = randint(*self.value_range)
        b = randint(*self.value_range)
        return a, b

    def _combine_operations(self):
        first_operation = True
        for i, x in enumerate(self.operation_seq):
            if first_operation:
                operation = Operation(x, Decimal(self.operand_seq[i]), Decimal(self.operand_seq[i+1]))
            else:
                operation = Operation(x, operation, Decimal(self.operand_seq[i+1]))
            first_operation = False
        return operation


if __name__ == "__main__":
    i = 0
    c = 0
    alive = True
    arithmetic = Question1()
    while alive:
        i += 1
        q = arithmetic.frame_question()
        question = q.sequence_str
        result = q.result
        message = f"{'#'*100} \n"
        message += f"QUESTION {str(i)}\n"
        message += f"{'#'*100} \n"
        puts(message)
        user_reply = prompt.query(f"{question} = ")
        message = f"{'='*100} \n"
        if user_reply == "exit":
            message += f"BYE! BYE!\n"
            alive = False
        elif Decimal(user_reply) == result:
            c += 1
            message += f"{colored.blue('You are RIGHT!')} => Score: {colored.blue(str(c)+' / '+str(i))}\n"
        else:
            message += f"{colored.red('You are WRONG!')} Correct answer is: {colored.red(result)}"
            message += f" => Score: {colored.blue(str(c)+' / '+str(i))}\n"
        puts(message)
