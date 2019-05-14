from random import sample, randint, choice
from decimal import Decimal
from fractions import Fraction
from .mixed_fractions import Mixed
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
    where a, b, c, d are
    (1) Integers
    (2) Proper / Improper fractions
    (3) Mixed Fractions
    (4) Decimal numbers

    """

    def __init__(self, operations=["/", "*", "+", "-"], operand_count=4, value_range=(0, 100), decimal_pt=0,
                 negative=False):
        self.operations = operations
        self.operand_count = operand_count
        self.decimal_pt = decimal_pt
        self.negative = negative
        self.value_range = value_range
        self.add_range = None
        self.div_range = None
        self.mul_range = None
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

    @property
    def decimal_pt(self):
        return self.__decimal_pt

    @decimal_pt.setter
    def decimal_pt(self, decimal_pt):
        self.__decimal_pt = decimal_pt

    @property
    def negative(self):
        return self.__negative

    @negative.setter
    def negative(self, negative):
        self.__negative = negative

    @property
    def value_range(self):
        return self.__value_range

    @value_range.setter
    def value_range(self, value_range):
        self.__value_range = value_range
        self._define_ranges()

    def _define_ranges(self):
        if self.decimal_pt == 1:
            self.add_range = [Decimal(x) / 10 for x in range(self.value_range[0]*10, self.value_range[1]*10)]
            self.mul_range = self.add_range
            self.div_range = [x for x in self.mul_range if Decimal(x) != 0]
        elif self.negative:
            self.add_range = list(range(*self.value_range))
            self.mul_range = list(range(int(-Decimal(self.value_range[1]).sqrt()),
                                        int(Decimal(self.value_range[1]).sqrt())))
            self.div_range = [x for x in self.mul_range if x != 0]
        else:
            self.add_range = list(range(*self.value_range))
            self.mul_range = list(range(int(Decimal(self.value_range[0]).sqrt()),
                                        int(Decimal(self.value_range[1]).sqrt())))
            self.div_range = [x for x in self.mul_range if x != 0]

    def frame_decimal_question(self):
        self.operand_seq = [None] * self.operand_count
        self.operation_seq = sample(self._sample_operations, self._operation_count)
        dividend_seq = [1]*self._operation_count
        for i, y in enumerate(self.operation_seq):
            if y == "/":
                if not self.operand_seq[i]:
                    self.operand_seq[i+1], self.operand_seq[i] = self._create_division()
                    dividend_seq[i] = self.operand_seq[i+1] * self.operand_seq[i]
                else:
                    self.operand_seq[i+1], _ = self._create_division(divisor=dividend_seq[i-1])
                    dividend_seq[i] = dividend_seq[i-1] * self.operand_seq[i+1]

        for i, y in enumerate(self.operation_seq):
            if y == "*":
                if not (self.operand_seq[i] or self.operand_seq[i+1]):
                    self.operand_seq[i], self.operand_seq[i+1] = self._create_multiplication()
                elif not self.operand_seq[i]:
                    self.operand_seq[i], _ = self._create_multiplication()
                elif not self.operand_seq[i+1]:
                    self.operand_seq[i+1], _ = self._create_multiplication()

        for i, y in enumerate(self.operation_seq):
            if y in ("+", "-"):
                if not (self.operand_seq[i] or self.operand_seq[i+1]):
                    self.operand_seq[i], self.operand_seq[i+1] = self._create_addition()
                elif not self.operand_seq[i]:
                    self.operand_seq[i], _ = self._create_addition()
                elif not self.operand_seq[i+1]:
                    self.operand_seq[i+1], _ = self._create_addition()

        self.operand_seq.reverse()
        self.operation_seq.reverse()
        self.question = self._combine_operations()
        return self.question

    def _create_division(self, divisor=None):
        if not divisor:
            divisor = choice(self.div_range)
        quotient = choice(self.div_range)
        dividend = quotient * divisor
        return Decimal(dividend), Decimal(divisor)

    def _create_multiplication(self):
        a = choice(self.mul_range)
        b = choice(self.mul_range)
        return Decimal(a), Decimal(b)

    def _create_addition(self):
        a = choice(self.add_range)
        b = choice(self.add_range)
        return Decimal(a), Decimal(b)

    def _combine_operations(self):
        first_operation = True
        for i, x in enumerate(self.operation_seq):
            if first_operation:
                operation = Operation(x, self.operand_seq[i], self.operand_seq[i+1])
            else:
                operation = Operation(x, operation, self.operand_seq[i+1])
            first_operation = False
        return operation

    def frame_fraction_question(self, mixed=False):
        self.operand_seq = [None] * self.operand_count
        self.operation_seq = sample(self._sample_operations, self._operation_count)
        self.operand_seq = self._create_random_fractions(self.operand_count)
        if mixed:
            self.operand_seq = [Mixed(x) for x in self.operand_seq]
        self.question = self._combine_operations()
        return self.question

    def _create_random_fractions(self, count):
        operand_seq = []
        for _ in range(count):
            numerator = choice(self.mul_range)
            denominator = choice(self.div_range)
            operand_seq.append(Fraction(numerator, denominator))
        return operand_seq


if __name__ == "__main__":
    i = 0
    c = 0
    alive = True
    arithmetic = Question1()
    while alive:
        i += 1
        x = randint(0, 15)
        arithmetic.negative = True
        if x % 4 == 0:
            arithmetic.decimal_pt = 0
            arithmetic.value_range = (0, 100)
            arithmetic.operand_count = 4
            q = arithmetic.frame_decimal_question()
        elif x % 4 == 1:
            arithmetic.operand_count = 3
            arithmetic.decimal_pt = 1
            arithmetic.value_range = (0, 10)
            q = arithmetic.frame_decimal_question()
        elif x % 4 == 2:
            arithmetic.decimal_pt = 0
            arithmetic.value_range = (1, 100)
            arithmetic.operand_count = 3
            q = arithmetic.frame_fraction_question()
        else:
            arithmetic.decimal_pt = 0
            arithmetic.value_range = (1, 100)
            arithmetic.operand_count = 3
            q = arithmetic.frame_fraction_question(mixed=True)
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
        elif user_reply.isalpha():
            message += f"ERROR!\n"
        else:
            if x % 4 in (0, 1):
                user_reply_formatted = Decimal(user_reply)
            else:
                user_reply_formatted = Mixed(user_reply)
            if user_reply_formatted == result:
                c += 1
                message += f"{colored.blue('You are RIGHT!')} => Score: {colored.blue(str(c)+' / '+str(i))}\n"
            else:
                message += f"{colored.red('You are WRONG!')} Correct answer is: {colored.red(result)}"
                message += f" => Score: {colored.blue(str(c)+' / '+str(i))}\n"
        puts(message)
