import math
import matplotlib.pyplot as plt
import numpy as np
import pylabo
pylabo.defaults()

B = 151.84

# Picos principales:
# B1 87
# B* 85
# A* 85
# A2 87

# freqs_hfs = {
#     "R85": { "A1": 8_945, "A2": 9_307, "B1": 5_909, "B2": 6_271, },
#     "R87": { "A1": 11_226, "A2": 12_040, "B1": 4_391, "B2": 5_205, }
# }

def delta_freq(gf, mf, B):
    return 1.3996 * gf * mf * B

def get_F(isot, state):
    f_85 = { "A": 2, "B": 3, "1": 2, "2": 3 }
    f_87 = { "A": 1, "B": 2, "1": 1, "2": 2 }

    if isot == "R85":
        return f_85[state]

    if isot == "R87":
        return f_87[state]

def get_g(isot, state):
    g_r85 = { "A": -1/3, "B": 1/3, "1": -1/9, "2": 1/9 }
    g_r87 = { "A": -1/2, "B": 1/2, "1": -1/6, "2": 1/6 }

    if isot == "R85":
        return g_r85[state]

    if isot == "R87":
        return g_r87[state]


def get_fs(isot):
    deviation = {}

    for fundam in ["A", "B"]:
        for exc in ["1", "2"]:
            f_a = get_F(isot, fundam)
            f_b = get_F(isot, exc)

            g_a = get_g(isot, fundam)
            g_b = get_g(isot, exc)

            freq = 1.3996 * math.fabs(f_a * g_a - f_b * g_b)

            transition = fundam + exc
            deviation[transition] = freq

    return deviation


r85 = get_fs("R85")
r87 = get_fs("R87")

teorico = {"R85": r85, "R87": r87}

ajustes = {
    "R85": {
        "A1": 0,
        "A2": 34.7,
        "B1": 39.7,
        "B2": 0
    },
    "R87": {
        "A1": 0,
        "A2": 41.9,
        "B1": 41.5,
        "B2": 0
    }
}

def calc_B(isot):
    transiciones = []
    campos = []
    # campos_err = []

    for trans in ajustes[isot].keys():
        freq_por_gauss = teorico[isot][trans]

        freq = ajustes[isot][trans]
        # freq_err = ajustes_err[isot][trans]

        if freq == 0:
            continue

        campo = freq / freq_por_gauss
        # campo_err = freq_err / freq_por_gauss

        transiciones.append(trans)
        campos.append(campo)
        # campos_err.append(campo_err)

    return transiciones, campos, 0


fig, ax = plt.subplots(2, 1, sharex=True)

for axis, isot in zip(ax, ["R85", "R87"]):
    transiciones, campos, campos_err = calc_B(isot)

    axis.bar(
        transiciones,
        campos,
        yerr=campos_err,
        capsize=5,
    )
    axis.set(ylabel=f"Campo magnético [G] ({isot})")

plt.tight_layout()
plt.show()
