import pylabo
import logging
from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

pylabo.logs.opts.level_console = logging.INFO
pylabo.defaults()
logger = logging.getLogger("main2")

data_path = Path("./data/14-4/primer bache")

SEC_TO_MICROSEC = 1_000_000


def get_ch(dfs, ch):
    channel = np.array([df[ch].to_numpy() for df in dfs])

    return channel


def compact(y, y0, n):
    core_size = y.size - 2 * n

    if y0.size == core_size:
        return y0

    if y0.size > core_size:
        pad = (y0.size - core_size) / 2

        left = math.floor(pad)
        right = -math.ceil(pad)

        # Remove up to n elements from each side
        return y0[left:right]

    logger.error(f"Reference array too small: {y0.size} < {core_size}")

def align(y, y0, n):
    # Make sure y0 has the right size
    y0 = compact(y, y0, n)

    distances = np.zeros(2 * n)

    for i in range(2 * n):
        y_shift = np.roll(y, -i)[:-2*n]

        # Distanced defined by the inner product
        distances[i] = np.linalg.norm(y_shift - y0)

    i_min =  np.argmin(distances)

    shift = n - i_min
    distance = distances[i_min]

    return shift, distance


def merge(ys, y0, n):
    y_shifted = []
    distances = []
    shifts = []

    for y in ys:
        shift, min_dist = align(y, y0, n=n)

        y_shift = np.roll(y, shift)[n:-n]

        y_shifted.append(y_shift)
        distances.append(min_dist)
        shifts.append(shift)

        y0 = compact(y, y0, n)

    y = np.mean(y_shifted, axis=0)
    shift = np.max(shifts)
    distance = np.mean(distances)

    return y, distance, shift


def compare_devs(path):
    dfs = [pd.read_csv(file) for file in path.glob("*.csv")]

    # tiempo = get_ch(dfs, "Tiempo") * SEC_TO_MICROSEC
    ch1 = get_ch(dfs, "Canal 1")
    # ch2 = get_ch(dfs, "Canal 2")

    y1 = np.mean(ch1, axis=0)
    # y02 = np.mean(ch2, axis=0)

    n = 120
    N = 20

    distances = []
    shifts = []

    fig, ax = plt.subplots(3, 1)

    for i in range(N):
        y1, dist, shift = merge(ch1, y1, n)

        distances.append(dist)
        shifts.append(shift)

        if len(distances) > 1:
            if distances[-1] == distances[-2]:
                break

    for y in ch1:
        ax[0].plot(y[n:-n], color="black", alpha=1/50)

    ax[0].set(title=path.name)
    ax[0].plot(y1, color="green", label="Sintetizado")
    ax[0].legend()
    ax[1].plot(distances)
    ax[2].plot(shifts)
    ax[1].set(ylabel="Dist")
    ax[2].set(ylabel="shift")
    plt.show()

    return y1, distances, shifts


for path in data_path.glob("*zeema*/"):
    y, dist, shift = compare_devs(path)
