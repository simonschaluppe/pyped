import numpy as np
import pandas as pd
from dataclasses import dataclass, field, fields, asdict
import pyped.excelLoader


@dataclass()
class TimeSeriesData:
    months: np.ndarray
    timesteps: int = 8760
    # climate
    TA: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "°C"})
    # solar gains
    QS: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "W/m²NGF"})
    # usage profiles
    QI: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "W/m²NGF",
        "description": "Qi Sommer W/m²"})

    # Ventilation
    ACH_V: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "ACH",
        "description": "Luftwechsel Ventilation"})

    # Infiltration
    ACH_I: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "ACH",
        "description": "Infiltrationsluftwechsel"})

    Qdhw: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "kWh/m²NGF"})

    QV: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "W/m²NGF"})
    QT: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "W/m²NGF"})

    Qh_min: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "W/m²NGF"})
    Qc_min: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "W/m²NGF"})
    # deckung abwärme?

    TI: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "°C"})
    Tdhc: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "ACH"})
    Ecars: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "%"})
    Batteries: np.ndarray = field(default=np.zeros(timesteps), metadata={
        "units": "%"})

    # Qx: list = field(default_factory=["QT","QV","QS","QI","Qh","Qc"])
    def list_qx(self) -> list:
        Qx_list = [self.QT,
                   self.QV,
                   self.QS,
                   self.QI,
                   self.Qh_min,
                   self.Qc_min]
        return Qx_list

    def qx_as_df(self):
        df_list = {"QT": self.QT,
                   "QV": self.QV,
                   "QS": self.QS,
                   "QI": self.QI,
                   "Qh_min": self.Qh_min,
                   "Qc_min": self.Qc_min}
        df = pd.DataFrame(df_list)
        return df

    def as_df(self):
        array_dict = {k: array for k, array in self.__dict__.items() if type(array) == np.ndarray}
        return pd.DataFrame(array_dict)

    def to_csv(self, path):
        self.as_df().to_csv(path)

    def load_csv(self, path="data/test/TSD_test.csv"):
        array = pd.read_csv(path, encoding="cp1252")
        for col in array.keys():
            if col in self.__dict__.keys():
                self.__dict__[col] = array[[col]].to_numpy().flatten()

    def to_excel(self, path):
        self.as_df().to_excel(path, sheet_name="TSD")

    def load_excel(self, path):
        excel_df = pd.read_excel(path, sheet_name="TSD")
        for col in excel_df.columns:
            if col in self.__dict__.keys():
                self.__dict__[col] = excel_df[[col]].to_numpy().flatten()


class Schedules():
    """
    PEEExcel
    """



@dataclass(order=True, unsafe_hash=True)
class Property(float):
    """PED property inluces a
    name: str
    value: float
    units: str = ""
    description: str = ""
    peexcel_id: str = ""
    zq_synergy_id: str = ""
    """
    name: str
    value: float
    units: str = ""
    description: str = ""
    peexcel_id: str = ""
    zq_synergy_id: str = ""

    def __new__(self, value, **kwargs):
        return float.__new__(self, value)

    def __repr__(self):
        return f"{self.value} [{self.units}]"

@dataclass
class SimInput_Category:
    def __init__(self, SimInput):
        self._SI = SimInput

class Category:
    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return self.__dict__.values().__iter__()

@dataclass
class Constants(Category):
    """
    Physik, etc.
    """
    cp_air: Property = field(default=Property(
        name="cp_air",
        value=0.34,
        units="Wh/m3K",
        description="Spez. Wärmekapazität Luft",
        peexcel_id="spez. Wärme kapazität Luft (Wh/m3K)"
        ))


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
        return self._SI["Anteil Lüftungsstrom wenn ohne Wärmerückgewinnung"]

    @property
    def hr_w(self):
        """Wirkungsgrad Wärmerückgewinnung (Winter)"""
        return self._SI["Wirkungsgrad Wärmerückgewinnung"]

    @property
    def cr_s(self):
        """Wirkungsgrad Wärmerückgewinnung (Winter)"""
        return self._SI["Wirkungsgrad Kälterückgewinnung"]

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


@dataclass
class DHW:
    T_min: float = field(default=60., metadata={
        "units": "°C"})
    T_max: float = field(default=70., metadata={
        "units": "°C"})
    efficiency_distribution: float = field(default=0.75, metadata={
        "units": "°C",
        "description": "Wirkungsgrad (Verteilungsverluste)"})

    storage_volume: float = field(default=10000., metadata={
        "units": "l",
        "description": "Wasserspeicher (l)"})

    storage_heat_loss: float = field(default=10000., metadata={
        "units": "W/K",
        "description": ""})

    heat_pump_power: float = field(default=7., metadata={
        "units": "W/m²NGF",
        "description": "Leistung Wärme pumpe (W/m²)"})

    efficiency_startup: float = field(default=0.75, metadata={
        "units": "°C",
        "description": "Wirkungsgrad (Verteilungsverluste)"})

    heat_pump_efficiency: float = field(default=3., metadata={
        "units": "",
        "description": "JAZ Wärme pumpe (W/m²)"})

    heating_efficiency: float = field(default=0.8, metadata={
        "units": "",
        "description": "Wirkungsgrad Aufheizen"})


@dataclass
class Plot:
    """
    Plot
    """
    residential:        float = field(default=0)
    commercial:         float = field(default=0)
    school:             float = field(default=0)
    kiga:               float = field(default=0)
    retail:             float = field(default=0)
    retail_food:        float = field(default=0)
    retail_nonfood:     float = field(default=0)

    net_floor_area:     float = field(default=0)

    net_storey_height: float = field(default=0, metadata={
        "units": "m",
        "description": "Durchschn. Raumhöhe für die Berechnung des Lüfungsvolumen (m)"})

    size: float = field(default=0, metadata={
        "units": "m²",
        "description": "Grundstücksfläche"})

    density: float = field(default=0.4, metadata={
        "units": "",
        "description": "GRZ"})

    fsi: float = field(default=0.4, metadata={
        "units": "",
        "description": "GFZ"})


@dataclass()
class PED:
    """
    Model of the PED
    """
    PEE_inputs: dict = field(default_factory=dict)

    Plot: Plot = field(default=Plot())
    Constants: Constants = field(default=Constants())
    ThermalHull: ThermalHull = field(default=ThermalHull(PEE_inputs))
    HeatingSystem: HeatingSystem = field(default=HeatingSystem(PEE_inputs))
    CoolingSystem: CoolingSystem = field(default=CoolingSystem(PEE_inputs))
    VentilationSystem: VentilationSystem = field(default=VentilationSystem(PEE_inputs))

    cI: float = 0

    @classmethod
    def from_PEExcel(cls, path="../data/PlusenergieExcel_Performance.xlsb"):
        PEE_inputs = pyped.excelLoader.load_inputs_from_PEExcel("../data/PlusenergieExcel_Performance.xlsb")

        # cI = self._SI["Speicherkapazität spezifisch Wirksame Wärmekapazität (Wh/m²K)"]
        return cls(
            PEE_inputs=PEE_inputs,
            Plot=Plot(
                    residential=PEE_inputs['Wohnbau NGF (m²)'],
                    commercial=PEE_inputs['Büro NGF (m²)'],
                    school=PEE_inputs['Schule NGF (m²)'],
                    kiga=PEE_inputs['Kiga NGF (m²)'],
                    retail=PEE_inputs['Handel NGF (m²)'],
                    retail_nonfood=PEE_inputs['Handel NGF (m²)'] * PEE_inputs['Anteil NonFood an Handel'],
                    retail_food= PEE_inputs['Handel NGF (m²)'] * (1 - PEE_inputs['Anteil NonFood an Handel']),
                    net_floor_area=PEE_inputs['Summe NGF (m²)'],
                    net_storey_height=PEE_inputs["Durchschn. Raumhöhe für die Berechnung des Lüfungs-volumen (m)"]),
            # Constants=Constants(),
            # ThermalHull=ThermalHull(PEE_inputs),
            # HeatingSystem=HeatingSystem(PEE_inputs),
            # CoolingSystem=CoolingSystem(PEE_inputs),
            # VentilationSystem=VentilationSystem(PEE_inputs),
            cI=PEE_inputs["Speicherkapazität spezifisch Wirksame Wärmekapazität (Wh/m²K)"],
                   )


if __name__ == "__main__":
    from pyped.excelLoader import load_inputs_from_PEExcel

    test_model = PED.from_PEExcel(path="../data/PlusenergieExcel_Performance.xlsb")

    # test_tsd = TimeSeriesData(months=np.genfromtxt("../data/profiles/months.csv"))
    # test_tsd.load_csv("../data/test/TSD_test.csv")
    a = test_model.Constants

