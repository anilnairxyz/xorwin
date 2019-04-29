from random import sample, choice
from primesieve import primes
from clint.textui import colored, puts, prompt


def prime_query(ratio=40, value_range=(1, 100)):
    i = choice(range(1, 100))
    p = primes(*value_range)
    a = [x for x in range(*value_range) if x not in p]
    if i <= ratio:
        return choice(p), True
    else:
        return choice(a), False


if __name__ == "__main__":
    i = 0
    c = 0
    alive = True
    while alive:
        i += 1
        query, is_prime = prime_query()
        message = f"{'#'*100} \n"
        message += f"QUESTION {str(i)}\n"
        message += f"{'#'*100} \n"
        puts(message)
        question = f"The HCF is: "
        question = f"Is {colored.cyan(query)} a prime number (Y/N): "
        reply = prompt.query(question)
        message = f"{'='*100} \n"
        if reply == "exit":
            message += f"BYE! BYE!\n"
            alive = False
        elif (reply in ("Y", "y") and is_prime) or (reply in ("N", "n") and not is_prime):
            c += 1
            message += f"{colored.blue('You are RIGHT!')} => Score: {colored.blue(str(c)+' / '+str(i))}\n"
        else:
            message += f"{colored.red('You are WRONG!')}"
            message += f" => Score: {colored.blue(str(c)+' / '+str(i))}\n"
        puts(message)
        message = f"{'='*100} \n"
