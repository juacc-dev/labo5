import pylabo
import logging
from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Estos tienen muy baja resolución
# descarte = [
#     "1776180553.5764189-con zeeman (diferencial y comun)",
#     "1776180377.3783967-con zeeman (diferencial y comun)",
# ]
pattern_dir = re.compile(r"(?P<code>\d*\.\d*)-(?P<name>.*)")
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

def show_all(data_path: Path):
    data_path = Path(data_path)

    for path in data_path.glob("*zeema*/"):
        # if path.name in descarte:
        #     continue

        x = pattern_dir.search(path.name)
        name = x.group("name")

        dfs = get_dfs(path)

        t = dfs[0]["Tiempo"] * 1000
        n = np.arange(len(dfs.keys()))

        ch1 = get_ch(dfs, "Canal 1")
        ch2 = get_ch(dfs, "Canal 2")

        fig, ax = plt.subplots(2, 1, sharex=True)

        for data1, data2 in zip(ch1, ch2):
            ax[0].plot(t, data1, color="black", alpha=0.07)
            ax[1].plot(t, data2, color="black", alpha=0.07)

        ax[0].set(title=name)
        plt.tight_layout()
        plt.show()

pylabo.logs.opts.level_console = logging.INFO
pylabo.defaults()
logger = logging.getLogger("main1")

show_all("./data/14-4/primer bache")
show_all("./data/14-4/segundo bache")

# x, y = np.meshgrid(t, n)

# fig = plt.figure()
# ax = plt.axes(projection="3d", computed_zorder=False)
# ax.plot_surface(
#     y,
#     x,
#     ch1,
#     label="Canal 1",
#     alpha=0.9,
# )

# ax.set(
#     ylabel="Tiempo [ms]",
#     xlabel="Núm. de med.",
#     zlabel="Señal [V]"
# )
# plt.legend()
