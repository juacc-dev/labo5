import pylabo
import logging
from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pylabo.logs.opts.level_console = logging.INFO
pylabo.defaults()
logger = logging.getLogger("main2")

data_path = Path("./data/14-4/primer bache")

pattern_files = re.compile(r"(?P<number>\d{1,2})\.csv")

def get_ch(dfs, ch):
    channel = np.zeros((
        len(dfs.keys()),
        dfs[0].shape[0]
    ))

    for n, df in dfs.items():
        channel[n] = df[ch].to_numpy()

    return channel

def get_dfs(path):
    dfs = {}
    for file in path.glob("*.csv"):
        x = pattern_files.search(file.name)
        n = int(x.group("number"))

        dfs[n] = pd.read_csv(file)

    return dfs


def fit_horizontal(x, y, y0, n):
    y0_test = [
        np.roll(y0, i)[n:-n]
        for i in range(-n, n)
    ]

    y_small = y[n:-n]

    distances = []
    for ref in y0_test:
        s = np.sqrt(np.sum((y_small - ref) ** 2))

        distances.append(s)

    i_min =  np.argmin(distances)
    # Negative sign implicit
    deviation = n - i_min

    return deviation, distances[i_min]


def compare_devs(path, n=50):
    dfs = get_dfs(path)

    tiempo = get_ch(dfs, "Tiempo") * 1000
    ch1 = get_ch(dfs, "Canal 1")
    ch2 = get_ch(dfs, "Canal 2")

    y01 = np.mean(ch1, axis=0)
    y02 = np.mean(ch2, axis=0)


    dist1 = []
    dist2 = []
    dev_rel = []

    for t, data1, data2 in zip(tiempo, ch1, ch2):
        dv1, s1 = fit_horizontal(t, data1, y01, n=n)
        dv2, s2 = fit_horizontal(t, data2, y02, n=n)

        dt = 1000 * (t[1] - t[0])
        dev_rel.append((dv2 - dv1) * dt)

        dist1.append(s1)
        dist2.append(s2)

    return dist1, dist2, dev_rel


for path in data_path.glob("*zeema*/"):
    dist1, dist2, dev_rel = compare_devs(path)

    fig, ax = plt.subplots(2, 1, sharex=True)

    ax[0].plot(dist1, label="Canal 1")
    ax[0].plot(dist2, label="Canal 2")

    ax[1].plot(dev_rel)

    ax[0].set(
        ylabel="Distancia a la referencia",
        title=f"{path.name}",
    )
    ax[1].set(
        xlabel="Número de archivo",
        ylabel=r"Desviación entre canales [$\mu$s]",
    )
    ax[0].legend()
    plt.tight_layout()
    plt.show()
