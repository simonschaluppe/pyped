
import pyped.datamodel
import numpy as np
import pandas as pd

from pyped.excelLoader import load_inputs_from_PEExcel



class Simulation():
    """
    :parameter:
    TimeSeriesData: Timeseries Data
    BuildingModel: building model (from PEEx
    """
    def __init__(self,
                 TimeSeriesData:pyped.datamodel.TimeSeriesData,
                 SimulationInput:dict,
                 ):
        self.TSD = TimeSeriesData # simulation result data
        self.SI = SimulationInput

        # Nutzungsprofile
        self.Usage = pd.read_csv("data/profiles/usage_profiles.csv", encoding="cp1252")

        #climate data
        self.TA = np.genfromtxt("data/profiles/climate.csv",
                                delimiter=";")[1:,1]
        # solar gains
        self.QS = np.genfromtxt("data/profiles/QS_test.csv") # W/m²
        self.QI = self.Usage["Qi Sommer W/m²"]

    def simulate(self):

        TI_min = self.SI["Heizung: Raumtemp.Minimum (°C)"]
        TI_max = self.SI["Kühlung Raumtemp.Minimum (°C)"]
        cI = self.SI["Speicherkapazität spezifisch Wirksame Wärmekapazität (Wh/m²K)"]  # Wh/m²K

        self.TSD.TI[0] = TI_min

        for t in range(1, 8760):
            self.calc_thermal_losses(t)

            # if self.TSD.TI[t] < TI_min:
            #     Qh[t] = (TI_min - TI[t]) * cI
            #     TI[t] = TI[t] + Qh[t] / cI
            #
            # if TI[t] > TI_max:
            #     Qc[t] = (TI_max - TI[t]) * cI
            #     TI[t] = TI[t] + Qc[t] / cI

    def calc_thermal_losses(self, t):
        dT = self.TA[t - 1] - self.TSD.TI[t - 1]

        self.TSD.QV[t] = self.calc_QV(self.Usage["Luftwechsel_Anlage_1_h"][t], dT)  # W/m²

        self.TSD.QT[t] = self.calc_QT(dT)  # W/m²

        Q_sum = (self.TSD.QT[t] + self.TSD.QV[t]) + self.QS[t] + self.QI[t]

        self.TSD.TI[t] = self.TSD.TI[t - 1] + Q_sum / self.SI["Speicherkapazität spezifisch Wirksame Wärmekapazität (Wh/m²K)"]  # Wh/m²K


    def calc_QT(self, dT):
        """Transmission heat losses [W/m²NGF]"""
        QT = self.SI["Transmission gesamt (W/K/m²NGF)"] * dT
        return QT

    def calc_QV(self, airchange, dT):
        """Ventilation losses [W/m²NGF]"""
        QV_dT = airchange * self.SI["Durchschn. Raumhöhe für die Berechnung des Lüfungs-volumen (m)"] * \
                self.SI["spez. Wärme kapazität Luft (Wh/m3K)"]
        QV = QV_dT * dT
        return QV




