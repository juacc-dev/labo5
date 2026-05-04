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

fgn = generador()

# %%

mult_v.write("CONFIGURE:VOLTAGE:DC")
mult_i.write("CONFIGURE:CURRENT:DC")

PRESION = 1  # milibar
DIST = 25.5  # mm

title = "barrido"
name = f"{title} {counter} - p={PRESION} mbar, d={DIST} mm"
counter += 1

N = 200
START = 0.3
STOP = 1.3

v_sets = np.logspace(np.log10(START), np.log10(STOP), N)

v_set_real = np.zeros(N)
v_e = np.zeros(N)
i = np.zeros(N)

# Corriente directa
fgn.set(shape=pylabo.visa.Tektronix_AFG3021B.Funs.DC)
# fgn.set(impedance=?)

t0 = time.time()

for n, v_set in enumerate(v_sets):
    fgn.set(voltage=v_set)

    time.sleep(1)
    v_set_real[n] = fgn.get_voltage()
    v_e[n] = mult_v.read()
    i[n] = mult_i.read()

    print_for_stats(i, N, t0, name)


total_time = time.time() - t0
mins = total_time // 60
secs = total_time % 60
print(f"Medición terminada en {mins:.0f} mins {secs:.0f} s")

df = pd.DataFrame({
    "V_set [s]": v_set_real,
    "Corriente [A]": i,
    "V_e [V]": v_e,
})

filename = DATA_DIR / name
df.to_csv(filename, index=False)


fig, ax = plt.subplots(3, 1)
ax[0].plot(v_set_real, v_e, ".")
ax[1].plot(v_set_real, i, ".")

ax[1].set(
    xlabel="Tensión del generador [V]",
    ylabel="Corriente [A]",
)
ax[0].set(
    xlabel="Tensión del generador [V]",
    ylabel="Tensión del tubo [V]",
)


ax[2].plot(i, v_e, ".")
ax[2].set(
    xlabel="Corriente [A]",
    ylabel="Tensión $V_e$ [V]",
    xscale="log",
)

plt.tight_layout()
plt.show()
