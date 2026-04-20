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

    deviation = n - np.argmin(distances)

    return deviation


path = Path(
    "./data/14-4/primer bache/1776179528.6044796-sin zeeman (canales separados)"
)

dfs = get_dfs(path)

tiempo = get_ch(dfs, "Tiempo") * 1000
ch1 = get_ch(dfs, "Canal 1")
ch2 = get_ch(dfs, "Canal 2")

# fig, ax = plt.subplots(2, 1, sharex=True)

y0 = ch1[0]
y02 = ch2[0]

for t, data1, data2 in zip(tiempo, ch1, ch2):
    n = 50
    dev = fit_horizontal(t, data1, y0, n=n)

    x_fit = t[n:-n]
    y_fit = np.roll(data1, dev)[n:-n]
    y2_fit = np.roll(data2, dev)[n:-n]

    fig, ax = plt.subplots(2, 1, sharex=True)

    ax[0].plot(t, y0, label="Referencia", color="black", alpha=0.8)
    ax[0].plot(t, data1, label="Señal original", color="red", alpha=0.3)
    ax[0].plot(x_fit, y_fit, label="Señal ajustada", color="green", alpha=0.8)

    ax[1].plot(t, y02, label="Referencia", color="black", alpha=0.8)
    ax[1].plot(t, data2, label="Señal original", color="red", alpha=0.3)
    ax[1].plot(x_fit, y2_fit, label="Señal ajustada", color="green", alpha=0.8)

    ax[0].set(xlim=((-3.5,  -0.5)))
    ax[1].set(xlim=((-3.5, -0.5)))
    ax[0].set(ylabel="Canal 1")
    ax[1].set(
        xlabel="Tiempo [ms]",
        ylabel="Canal 2"
    )

    ax[0].legend()
    plt.tight_layout()
    plt.show()
