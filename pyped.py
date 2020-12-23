
#
# import pyped.read
# TA = pyped.read.Profile.read_climate("data/profiles/climate.csv") ## relative path from here
#


import numpy as np
import matplotlib.pyplot as plt


TA  = np.genfromtxt("data/profiles/climate.csv",
    delimiter=";")[1:,1]

QS = np.genfromtxt("data/profiles/QS_test.csv") # W/m²

# QS = 9.95 * np.ones((8760,1))
QI = 4.76 * np.ones((8760,1))   # W/m²

QV_dT = 0.5  #W/K/m2
QV = np.zeros((8760,1))

QT_dT = 0.7   # W/K/m²
cI = 200        # Wh/m²K

QT = np.zeros((8760,1))

TI = np.zeros(8760)
TI[0] = 15.

for t in range(1, 8760):
    dT =  TA[t-1] - TI[t-1]
    QV[t] = QV_dT * dT # W/m²
    QT[t] = QT_dT * dT # W/m²
    Q_sum = (QT[t] + QV[t]) + QS[t] + QI[t]
    TI[t] = TI[t-1] + Q_sum/cI
    print(t, TA[t], QS[t], TA[t]+QS[t])


# plt.plot(TA)
plt.clf()
plt.plot(TI)
plt.plot(TA)
plt.legend(["TI","TA"])
plt.show()

plt.plot(QT)
plt.plot(QV)
plt.plot(QS)
plt.plot(QI)
plt.show()
