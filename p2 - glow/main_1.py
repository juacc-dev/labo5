import pylabo
import matplotlib.pyplot as plt
import time
from pathlib import Path
import numpy as np
import pandas as pd

from config import print_for_stats, multimetros, generador, DATA_DIR, logger

counter = 0

# %%

mult_v, mult_i = multimetros()

# fgn = generador()

# %%

mult_v.write("CONFIGURE:VOLTAGE:DC")
mult_i.write("CONFIGURE:CURRENT:DC")

PRESION = 1  # milibar
DIST = 25.5  # mm

title = "medicion"
name = f"{title} {counter} - p={PRESION} mbar, d={DIST} mm"
counter += 1

N = 300

t = np.zeros(N)
volt = np.zeros(N)
corr = np.zeros(N)

t0 = time.time()

for i in range(N):
    t[i] = time.time() - t0
    volt[i] = mult_v.read()
    corr[i] = mult_i.read()

    print_for_stats(i, N, t0, name)

total_time = time.time() - t0

mins = total_time // 60
secs = total_time % 60

print(f"\nMedición terminada en {mins:.0f} mins {secs:.0f} s")

df = pd.DataFrame({
    "Tiempo [s]": t,
    "Corriente [A]": corr,
    "Tensión [V]": volt,
})

filename = DATA_DIR / name
logger.info(f"Guardando {filename}")

df.to_csv(filename, index=False)


fig, ax = plt.subplots(3, 1)
ax[0].plot(t/60, volt, ".", label="Tensión")
ax[1].plot(t/60, corr, ".", label="Corriente")
ax[1].set(
    xlabel="Tiempo [min]",
    ylabel="Corriente [A]"
)
ax[0].set(ylabel="Tensión [V]")

ax[2].plot(corr, volt, ".")
ax[2].set(
    xlabel="Corriente [A]",
    ylabel="Tensión [V]",
    xscale="log",
)

plt.tight_layout()
plt.show()
