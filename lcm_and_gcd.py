from random import sample
from clint.textui import colored, puts, prompt


def gcd_calc(a, b):
    """GCD of a and b using the Euclidean algorithm"""
    if a == 0:
        return b
    return gcd_calc(b % a, a)


def lcm_calc(a, b):
    """LCM of a and b using the GCD"""
    return a * b // gcd_calc(a, b)


def lcm_gcd_query(value_range=(1, 100)):
    query_nos = sample(range(*value_range), 2)
    return query_nos, gcd_calc(*query_nos), lcm_calc(*query_nos)


if __name__ == "__main__":
    i = 0
    s = 0
    c = 0
    alive = True
    while alive:
        i += 1
        s += 1
        query, gcd, lcm = lcm_gcd_query((1, 50))
        message = f"{'#'*100} \n"
        message += f"QUESTION {str(i)}\n"
        message += f"{'#'*100} \n"
        message += f"Find the GCD and LCM of: {colored.cyan('  '.join([str(x) for x in query]))}\n"
        puts(message)
        question = f"The GCD is: "
        gcd_reply = prompt.query(question)
        message = f"{'='*100} \n"
        if gcd_reply == "exit":
            message += f"BYE! BYE!\n"
            alive = False
            continue
        elif int(gcd_reply) == gcd:
            c += 1
            message += f"{colored.blue('You are RIGHT!')} => Score: {colored.blue(str(c)+' / '+str(s))}\n"
        else:
            message += f"{colored.red('You are WRONG!')} Correct answer is: {colored.red(gcd)}"
            message += f" => Score: {colored.blue(str(c)+' / '+str(s))}\n"
        puts(message)
        s += 1
        message = f"{'='*100} \n"
        question = f"The LCM is: "
        lcm_reply = prompt.query(question)
        if lcm_reply == "exit":
            message += f"BYE! BYE!\n"
            alive = False
        elif int(lcm_reply) == lcm:
            c += 1
            message += f"{colored.blue('You are RIGHT!')} => Score: {colored.blue(str(c)+' / '+str(s))}\n"
        else:
            message += f"{colored.red('You are WRONG!')} Correct answer is: {colored.red(lcm)}"
            message += f" => Score: {colored.blue(str(c)+' / '+str(s))}\n"
        puts(message)
