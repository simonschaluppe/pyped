
#
# import pyped.read
# TA = pyped.read.Profile.read_climate("data/profiles/climate.csv") ## relative path from here
#


import numpy as np
import pandas as pd
import pyped.datamodel, pyped.Plot, pyped.simulation
from pyped.excelLoader import load_inputs_from_PEExcel



#def simulate():
TA  = np.genfromtxt("data/profiles/climate.csv",
    delimiter=";")[1:,1]

QS = np.genfromtxt("data/profiles/QS_test.csv") # W/m²

# PEExcel "Energiesumme"
Usage = pd.read_csv("data/profiles/usage_profiles.csv", encoding="cp1252")
QI = Usage["Qi Sommer W/m²"]

# PEExcel "Sim"
SI = load_inputs_from_PEExcel("data/PlusenergieExcel_Performance.xlsb")
M = pyped.datamodel.Model(SI)


# QV_dT [W/m²K] = luftwechsel [1/h] * raumhöhe [m] * cp_luft [Wh/m³K] > [W/m²K]
QV_dT = Usage["Luftwechsel_Anlage_1_h"] * SI["Durchschn. Raumhöhe für die Berechnung des Lüfungs-volumen (m)"] * SI["spez. Wärme kapazität Luft (Wh/m3K)"]

QV = np.zeros(8760)

QT_dT = SI["Transmission gesamt (W/K/m²NGF)"] # W/K/m²
cI = SI["Speicherkapazität spezifisch Wirksame Wärmekapazität (Wh/m²K)"] # Wh/m²K

QT = np.zeros(8760)

TI_min = SI["Heizung: Raumtemp.Minimum (°C)"]
TI_max = SI["Kühlung Raumtemp.Minimum (°C)"]

TI = np.zeros(8760)
TI[0] = TI_min


Qh = np.zeros(8760)
Qc = np.zeros(8760)

for t in range(1, 8760):
    dT =  TA[t-1] - TI[t-1]
    QV[t] = QV_dT[t] * dT # W/m²
    QT[t] = QT_dT * dT # W/m²
    Q_sum = (QT[t] + QV[t]) + QS[t] + QI[t]
    TI[t] = TI[t-1] + Q_sum / cI
    if TI[t] < TI_min:
        Qh[t] = (TI_min - TI[t]) * cI
        TI[t] = TI[t] + Qh[t] / cI

    if TI[t] > TI_max:
        Qc[t] = (TI_max - TI[t]) * cI
        TI[t] = TI[t] + Qc[t] / cI


# plt.plot(TA)



pyped.Plot.plot_Temp_Q(TI,TA,QT,QV,QS,QI,Qh,Qc,QV_dT)


#DSM Sim
for t in range(1, 8760):
    pass







if __name__ == "__main__":
    SI = load_inputs_from_PEExcel("data/PlusenergieExcel_Performance.xlsb")
    TSD = pyped.datamodel.TimeSeriesData()
    sim = pyped.simulation.Simulation(TSD, SI)
    sim.simulate()
    pyped.Plot.plot_Temp_Q(sim.TSD.TI, sim.TA)



