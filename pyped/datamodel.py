
import numpy as np
import pandas as pd
from pyped.excelLoader import load_inputs_from_PEExcel
from collections import namedtuple


class TimeSeriesData():
    """
    puh eh
    """
    def __init__(self, timesteps:int=8760):
        self.timesteps = timesteps
        self.months = np.genfromtxt("data/profiles/months.csv")
        #climate
        self.TA = np.zeros(timesteps)
        #solar gains
        self.QS = np.zeros(timesteps)
        #usage profiles
        self.QI = np.zeros(timesteps)
        self.ACH_V = np.zeros(timesteps) #Ventilation
        self.ACH_I = np.zeros(timesteps) #Infiltration
        self.Qdhw   = np.zeros(timesteps)


        self.QV = np.zeros(timesteps)
        self.QT = np.zeros(timesteps)

        self.Qh_min = np.zeros(timesteps)
        self.Qc_min = np.zeros(timesteps)
        # deckung abwärme?

        self.TI = np.zeros(timesteps)
        self.Tdhc = np.zeros(timesteps)
        self.Ecars = np.zeros(timesteps)
        self.Batteries = np.zeros(timesteps)

class Schedules():
    """
    PEEExcel
    """


class SimInput_Category():
    def __init__(self, SimInput):
        self._SI = SimInput

class Constants(SimInput_Category):
    """
    Physik, etc.
    """
    @property
    def cp_air(self):
        """
        spez. Wärmekapazität Luft (Wh/m3K)
        :return: (Wh/m3K)
        """
        return self._SI["spez. Wärme kapazität Luft (Wh/m3K)"]

class Size(SimInput_Category):
    """
    [m²NGF]
    Nettogeschoßflächen der Nutzungen

    """
    def __init__(self, SimInput):
        self._SI = SimInput
        self.residential = SimInput['Wohnbau NGF (m²)']
        self.commercial  = SimInput['Büro NGF (m²)']
        self.school      = SimInput['Schule NGF (m²)']
        self.kiga        = SimInput['Kiga NGF (m²)']
        self.retail      = SimInput['Handel NGF (m²)']
        self.retail_pc_nonfood = SimInput['Anteil NonFood an Handel']
        self.retail_food = self.retail * (1 - self.retail_pc_nonfood)
        self.retail_nonfood = self.retail * self.retail_pc_nonfood

        self.sum = SimInput['Summe NGF (m²)']

    @property
    def rh(self):
        "Durchschn. Raumhöhe für die Berechnung des Lüfungsvolumen (m)"
        return self._SI["Durchschn. Raumhöhe für die Berechnung des Lüfungs-volumen (m)"]

class ThermalHull(SimInput_Category):
    @property
    def QT_dT(self):
        """Transmission gesamt (W/K/m²NGF)"""
        return self._SI["Transmission gesamt (W/K/m²NGF)"]

class HeatingSystem(SimInput_Category):
    @property
    def minimum_room_temperature(self):
        """Heizung: Raumtemp.Minimum (°C)"""
        return self._SI["Heizung: Raumtemp.Minimum (°C)"]
    @property
    def maximum_room_temperature(self):
        """Heizung: Raumtemp.Maximum (°C)"""
        return self._SI["Heizung: Raumtemp.Maximum (°C)"]

class CoolingSystem(SimInput_Category):
    @property
    def minimum_room_temperature(self):
        """
        Kühlung Raumtemp.Minimum (°C)
        Ist die höchste zulässige Temperatur
        """
        return self._SI["Kühlung Raumtemp.Minimum (°C)"]

    @property
    def maximum_room_temperature(self):
        """Kühlung Raumtemp.Maximum (°C)"""
        return self._SI["Kühlung Raumtemp.Maximum (°C)"]

class VentilationSystem(SimInput_Category):
    @property
    def share_cs(self):
        """Lüftungs- und Luftvolumen-Anteil ohne Wärmerückgewinnung"""
        return self._SI["Lüftungsanteil ohne Wärmerückgewinnung"]

    @property
    def hr_w(self):
        """Wirkungsgrad Wärmerückgewinnung (Winter)"""
        return self._SI["Wirkungsgrad Wärmerückgewinnung"]\

    @property
    def cr_s(self):
        """Wirkungsgrad Wärmerückgewinnung (Winter)"""
        return self._SI["Wirkungsgrad Kälterückgewinnung"]\

    @property
    def hr_t(self):
        """Wirkungsgrad Wärmerückgewinnung (Winter)"""
        return self._SI["Wirkungsgrad Übergangszeit"]

    @property
    def use_heat_recovery(self) -> bool:
        """Lüftungsanlage"""
        if self._SI["Lüftungsanlage"] == "WAHR":
            return True
        else:
            return False

    @property
    def use_ventilation(self) -> bool:
        """Lüftungsanlage"""
        if self._SI["Lüftungsanlage"] == "WAHR":
            return True
        else:
            return False

class Model():
    """
    Model of the PEExcel Simulation Input
    """
    def __init__(self, SimInput):
        self._SI = SimInput

        self.size = Size(SimInput)

        self.const = Constants(SimInput)

        self.hull = ThermalHull(SimInput)

        self.heat = HeatingSystem(SimInput)

        self.cool = CoolingSystem(SimInput)

        self.vent = VentilationSystem(SimInput)

    def __repr__(self):
        return "Model of the PEExcel Simulation Input"
        """Speicherkapazität spezifisch Wirksame Wärmekapazität (Wh/m²K)"""

    @property
    def cI(self):
        return self._SI["Speicherkapazität spezifisch Wirksame Wärmekapazität (Wh/m²K)"]





if __name__ == "__main__":
    SI = load_inputs_from_PEExcel("data/PlusenergieExcel_Performance.xlsb")
    test_model = Model(SI)
