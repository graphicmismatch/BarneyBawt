import math


def solve(eqn):
    return eval(simplify(eqn))


def simplify(eqn):
    p = str(eqn).replace("pi", "3.141592653589793")
    p = p.replace("e", "2.718281828459045")
    p = p.replace("[", "(")
    p = p.replace("]", ")")
    p = p.replace("{", "(")
    p = p.replace("}", ")")
    p = p.replace("sin", "s")
    p = p.replace("cos", "c")
    p = p.replace("tan", "t")
    p = p.replace("cot", "o")
    p = p.replace("sec", "x")
    p = p.replace("csc", "y")
    p = p.replace("rad", "r")
    p = p.replace("^", "**")
    op = {"s", "c", "t", "o", "x", "y", "r"}
    startindex = -1
    endindex = -1
    offset = 1
    if ")" in p:
        while ")" in p:
            endindex = p.find(")")
            endindex += 1
            while True:
                if p[(endindex - offset)] == "(":
                    startindex = endindex - offset
                    break
                else:
                    offset += 1
            if p[startindex - 1] in op:
                p = p.replace(
                    p[startindex - 1:endindex],
                    str(doFunc(p[startindex - 1], p[startindex:endindex])))
            else:
                p = p.replace(p[startindex:endindex],
                              str(solve(p[startindex:endindex])))
    return p


def doFunc(act, eqn):
    val = solve(eqn)
    if act == "r":
        return math.radians(val)
    if act == "s":
        return math.sin(val)
    if act == "c":
        return math.cos(val)
    if act == "t":
        return math.tan(val)
    if act == "o":
        return 1 / math.tan(val)
    if act == "x":
        return 1 / math.cos(val)
    if act == "y":
        return 1 / math.sin(val)
