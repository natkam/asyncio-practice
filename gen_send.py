"""
Two simple examples of generators, using the `send` method.
See this article: https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/
"""

def bottom():
    print("to the bottom")
    return (yield 42)

def middle():
    print("through middle")
    return (yield from bottom())

def top():
    print("From top")
    return (yield from middle())


##############################
def jumping_range(up_to):
    idx = 0
    while idx < up_to:
        jump = yield idx
        if jump is None:
            jump = 1
        idx += jump


if __name__ == '__main__':
    g = top()
    value = next(g)
    print(value)

    try:
        value = g.send(value * 2)
    except StopIteration as exc:
        value = exc.value
    print(value)

    ###############
    print("\n##############################\n")
    ###############
    it = jumping_range(5)
    print(next(it))
    print(it.send(2))
    print(next(it))
    print(next(it))
    print(it.send(-3))
    print("\n")

    for _ in it:
        print(_)
