import pylabo
import matplotlib.pyplot as plt
import logging
import time
from pathlib import Path
import numpy as np
import pandas as pd

pylabo.logs.opts.level_console = logging.INFO
pylabo.defaults()

logger = logging.getLogger("main")

DATA_DIR = Path(r"C:\Users\publico\Documents\L5G5\data\04-5")

MULT1_ADDR = "GPIB0::22::INSTR"
MULT2_ADDR = "GPIB0::23::INSTR"

FGN_ADDR = "USB0::0x0699::0x0346::C036492::INSTR"

DATA_DIR.mkdir(exist_ok=True, parents=True)

logging.info(f"Usando directorio {DATA_DIR}")


def multimetros():
    mult_v = pylabo.visa.Agilent_34401A(MULT1_ADDR)
    logger.info(f"Conectado al multímetro {mult_v.query('*IDN?')}")

    mult_i = pylabo.visa.Agilent_34401A(MULT2_ADDR)
    logger.info(f"Conectado al multímetro {mult_i.query('*IDN?')}")

    return mult_v, mult_i

def generador():
    fgn = pylabo.visa.Tektronix_AFG3021B(FGN_ADDR)
    logger.info(f"Conectado al generador {fgn.query('*IDN?')}")

    return fgn


def print_for_stats(i, N, t0, name):
    percent = 100 * (i + 1) / N
    t = time.time() - t0
    rate = (i + 1) / t
    eta = (N - i - 1) / rate

    print("\x1b[2K", end="")
    print(
        f"Midiendo \x1b[38;2;255;255;30m{name}\x1b[0m, {percent:.0f}% \x1b[37m(ETA {eta:.0f}s)\x1b[0m", end="")
