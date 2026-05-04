B = 70

MU_B_H = 1.3996  # Magnetón de Bohr sobre constant de Planck

R85 = "R85"
R87 = "R87"

F = {
    R85: { "A": 2, "B": 3, "1": 2, "2": 3 },
    R87: { "A": 1, "B": 2, "1": 1, "2": 2 }
}

g_F = {
    R85: { "A": -1/3, "B": 1/3, "1": -1/9, "2": 1/9 },
    R87: { "A": -1/2, "B": 1/2, "1": -1/6, "2": 1/6 }
}

abs = lambda x: x if x > 0 else -x


def get_freq(isot: str, transition: str):
    fundam = transition[0]
    exc = transition[1]

    f_a = F[isot][exc]
    f_b = F[isot][fundam]

    g_a = g_F[isot][exc]
    g_b = g_F[isot][fundam]

    freq = 2 * B * MU_B_H * abs(f_a * g_a - f_b * g_b)

    return freq


for isot in [R85, R87]:
    print(f"{isot} = " + "{")

    for transition in ["A1", "A2", "B1", "B2"]:
        freq = get_freq(isot, transition)

        print(f"  \"{transition}\": {freq:.2f},")

    print("}")
