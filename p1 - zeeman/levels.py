import math
B = 70

def delta_freq(gf, mf, B):
    return 1.4 * gf * mf * B


def g_J(L, J):
    if L == 0 and J == 1/2:
        return 2.002

    if L == 1:
        if J == 1/2:
            return 0.666

        if J == 3/2:
            return 1.334

    return 0


def g_F(L, J, I, F):
    i2 = I * (I + 1)
    j2 = J * (J + 1)
    f2 = F * (F + 1)

    gj = g_J(L, J)

    if gj == 0:
        return 0

    if F == 0:
        return 0

    return gj * (f2 - i2 + j2) / (2 * f2)

def state(L, J):
    if L == 0 and J == 1/2:
        return "fundam"

    if L == 1:
        if J == 1/2:
            return "D1"

        if J == 3/2:
            return "D2"

    return ""


def get_fs(isot):
    print(f"# {isot}")

    if isot == "R85":
        FS = {
            "fundam": [2, 3],
            "D1": [2, 3],
            "D2": [1, 2, 3, 4],
        }
        I = 5/2

    elif isot == "R87":
        FS = {
            "fundam": [1, 2],
            "D1": [1, 2],
            "D2": [0, 1, 2, 3],
        }
        I = 3/2

    else:
        return

    LS = [0, 1]
    JS = [1/2, 3/2]

    for L in LS:
        for J in JS:
            s = state(L, J)
            if s == "" or s == "D2":
                continue

            print(f"\n## {s}")

            for F in FS[s]:
                gf = g_F(L, J, I, F)
                freq = delta_freq(gf, F, B)

                print(f"F = {F}\t-> {math.fabs(freq):.3f} MHz")


get_fs("R85")
print("")
get_fs("R87")
