
import numpy as np
from pyped.excelLoader import load_inputs_from_PEExcel
from collections import namedtuple


class TimeSeriesData():
    """
    puh eh
    """
    def __init__(self, timesteps:int=8760):
        self.timesteps = timesteps

        self.QV = np.zeros(timesteps)
        self.QT = np.zeros(timesteps)

        self.Qh_min = np.zeros(timesteps)
        self.Qc_min = np.zeros(timesteps)
        self.Qdhw   = np.zeros(timesteps)
        # deckung abwärme?

        self.TI = np.zeros(timesteps)
        self.Tdhc = np.zeros(timesteps)
        self.Ecars = np.zeros(timesteps)
        self.Batteries = np.zeros(timesteps)


class Area():
    """
    [m²NGF]
    Nettogeschoßflächen der Nutzungen

    """
    residential: float

    def __init__(self, SimInput):

        self.residential = SimInput['Wohnbau NGF (m²)']
        self.commercial  = SimInput['Büro NGF (m²)']
        self.school      = SimInput['Schule NGF (m²)']
        self.kiga        = SimInput['Kiga NGF (m²)']
        self.retail      = SimInput['Handel NGF (m²)']
        self.retail_pc_nonfood = SimInput['Anteil NonFood an Handel']
        self.retail_food = self.retail * (1 - self.retail_pc_nonfood)
        self.retail_nonfood = self.retail * self.retail_pc_nonfood

        self.sum = SimInput['Summe NGF (m²)']

class Model():
    """
    Model of the PEExcel Simulation Input
    """

    area: Area #ladida

    def __init__(self, SimInput):
        self.area = Area(SimInput)
    def __repr__(self):
        return "Model of the PEExcel Simulation Input"

if __name__ == "__main__":
    SI = load_inputs_from_PEExcel("data/PlusenergieExcel_Performance.xlsb")

    test_model = Model(SI)
