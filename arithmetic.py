from random import sample, randint
from decimal import Decimal
from fractions import Fraction
from mixed_fractions import Mixed
from clint.textui import colored, puts, prompt


class Operation:

    def __init__(self, operation="+", operand=(0, 0)):

        self.sequence = None
        self.result = None
        self.formula = []
        self.printable = []

        if operation in ("+", "-", "*", "/"):
            self.sequence = {"operation": operation, "operand": []}
            if isinstance(operand[0], Operation):
                self.sequence["operand"].append(operand[0].sequence)
                self.formula.append(operand[0].formula)
                self.printable.append(operand[0].printable)
            else:
                self.sequence["operand"].append(operand[0])
                self.formula.append(repr(operand[0]))
                self.printable.append(str(operand[0]))
            self.formula.append(f" {operation} ")
            self.printable.append(f" {operation} ")

            if isinstance(operand[1], Operation):
                self.sequence["operand"].append(operand[1].sequence)
                self.formula.append(operand[1].formula)
                self.printable.append(operand[1].printable)
            else:
                self.sequence["operand"].append(operand[1])
                self.formula.append(repr(operand[1]))
                self.printable.append(str(operand[1]))

        elif operation == "square":
            self.sequence = {"operation": operation, "operand": []}
            if isinstance(operand, Operation):
                self.sequence["operand"].append(operand.sequence)
                self.formula.append(operand.formula)
                self.printable.append(operand.printable)
            else:
                self.sequence["operand"].append(operand)
                self.formula.append(repr(operand))
                self.printable.append(str(operand))
            self.formula.append(" ** 2 ")
            self.printable.append(" ** 2 ")

        elif operation == "bracket":
            self.sequence = {"operation": operation, "operand": []}
            if isinstance(operand, Operation):
                self.sequence["operand"].append(operand.sequence)
                self.formula.append(" (")
                self.formula.append(operand.formula)
                self.formula.append(") ")
                self.printable.append(" (")
                self.printable.append(operand.printable)
                self.printable.append(") ")
            else:
                raise ValueError("Bracket can only be performed only over another Operation")

        else:
            raise ValueError("Unsupported Operation")

        self.formula = "".join(x for x in self.formula)
        self.printable = "".join(x for x in self.printable)
        self.printable = self.printable.replace("/", "\u00F7")
        self.result = eval(self.formula)


class Question1:

    def __init__(self):
        self.allowed_operations = ["/", "*", "+", "-"]
        self.operand_count = 4
        self.range = (1, 100)
        self.operand_seq = [None]*self.operand_count
        self.operation_seq = sample(self.allowed_operations * 2, self.operand_count-1)

        for i, y in enumerate(self.operation_seq):
            if y == "/":
                if not self.operand_seq[i]:
                    self.operand_seq[i+1], self.operand_seq[i] = self._create_division()
                else:
                    self.operand_seq[i+1], _ = self._create_division(divisor=self.operand_seq[i])

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
        self.question = self.frame_question()

    def _create_division(self, divisor=None):
        if not divisor:
            divisor = randint(self.range[0], Decimal(self.range[1]).sqrt())
        quotient = randint(self.range[0], Decimal(self.range[1]).sqrt())
        dividend = quotient * divisor
        return dividend, divisor

    def _create_multiplication(self):
        a = randint(self.range[0], Decimal(self.range[1]).sqrt())
        b = randint(self.range[0], Decimal(self.range[1]).sqrt())
        return a, b

    def _create_addition(self):
        a = randint(*self.range)
        b = randint(*self.range)
        return a, b

    def frame_question(self):
        first_operation = True
        for i, x in enumerate(self.operation_seq):
            if first_operation:
                operation = Operation(x, (Decimal(self.operand_seq[i]), Decimal(self.operand_seq[i+1])))
            else:
                operation = Operation(x, (operation, Decimal(self.operand_seq[i+1])))
            first_operation = False
        return operation


if __name__ == "__main__":
    i = 0
    c = 0
    alive = True
    while alive:
        i += 1
        q = Question1()
        question = q.question.printable
        result = q.question.result
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
