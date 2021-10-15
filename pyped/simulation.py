import numpy as np
import pandas as pd

import pyped.datamodel


class Simulation():
    """
    :parameter:
    TimeSeriesData: Timeseries Data
    BuildingModel: building model (from PEEx
    """

    def __init__(self,
                 TimeSeriesData: pyped.datamodel.TimeSeriesData,
                 SimulationInput: dict,
                 ):
        self.TSD = TimeSeriesData  # simulation result data
        self.SI = SimulationInput

        # Nutzungsprofile
        self.Usage = pd.read_csv("data/profiles/usage_profiles.csv", encoding="cp1252")

        # climate data
        self.TA = np.genfromtxt("data/profiles/climate.csv",
                                delimiter=";")[1:, 1]
        # solar gains
        self.QS = np.genfromtxt("data/profiles/QS_test.csv")  # W/m²
        self.QI = self.Usage["Qi Sommer W/m²"]


def simulate(M: pyped.datamodel.PED, TSD: pyped.datamodel.TimeSeriesData) -> pyped.datamodel.TimeSeriesData:
    cI = M.cI  # speicherkapazität
    TI_min = M.HeatingSystem.minimum_room_temperature
    TI_max = M.CoolingSystem.minimum_room_temperature
    TSD.TI[0] = TI_min


    #mainloop
    for t in range(1, 8760):

        TSD.QV[t] = calc_QV(M, TSD, t)
        ##
        TSD.QT[t] = calc_QT(M, TSD, t)

        Q_sum = (TSD.QT[t] + TSD.QV[t]) + TSD.QS[t] + TSD.QI[t]
        TSD.TI[t] = TSD.TI[t - 1] + Q_sum / M.cI
        TI_min = M.HeatingSystem.minimum_room_temperature
        TI_max = M.CoolingSystem.minimum_room_temperature

        if TSD.TI[t] < TI_min and is_heating_season(M, TSD, t):
            TSD.Qh_min[t] = (TI_min - TSD.TI[t]) * M.cI
            # TSD.TI[t] = TSD.TI[t] + TSD.Qh[t] / M.cI
            TSD.TI[t] = TI_min

        if TSD.TI[t] > TI_max and is_cooling_season(M, TSD, t):
            TSD.Qc_min[t] = (TI_max - TSD.TI[t]) * M.cI
            # TSD.TI[t] = TSD.TI[t] + TSD.Qc[t] / M.cI
            TSD.TI[t] = TI_max

        # calc_DHW(M, TSD, t)
    return TSD

def is_heating_season(M, TSD, t):
    if TSD.months[t] <= 4 or TSD.months[t] >= 10:
        return True
    else:
        return False


def is_cooling_season(M, TSD, t):
    if 5 <= TSD.months[t] <= 8:
        return True
    else:
        return False


def calc_QV(M, TSD, t):
    """Ventilation losses [W/m²NGF]"""
    dT = TSD.TA[t - 1] - TSD.TI[t - 1]
    room_height = M.Plot.net_storey_height
    cp_air = M.Constants.cp_air

    # thermally effective air change

    if M.VentilationSystem.use_heat_recovery:
        if is_heating_season(M, TSD, t):
            # heat recovery
            eff_share_after_heat_recovery = 1 - M.VentilationSystem.hr_w  # relative to unrecovered
        elif is_cooling_season(M, TSD, t):
            # cool recovery
            eff_share_after_heat_recovery = 1 - M.VentilationSystem.cr_s  # relative to unrecovered
        else:
            # heat recovery
            eff_share_after_heat_recovery = 1 - M.VentilationSystem.cr_s  # relative to unrecovered
    else:
        rel_ACH_after_heat_recovery = 1  # relative to unrecovered
    eff_airchange = TSD.ACH_I[t] \
                    + TSD.ACH_V[t] * M.VentilationSystem.share_cs \
                    + TSD.ACH_V[t] * (1 - M.VentilationSystem.share_cs) * rel_ACH_after_heat_recovery

    QV = eff_airchange * room_height * cp_air * dT
    return QV



def calc_QT(M, TSD, t):
    dT = TSD.TA[t - 1] - TSD.TI[t - 1]
    QT = M.ThermalHull.QT_dT * dT
    return QT


def calc_DHW(M, TSD, t):
    """=WENN(Q56<$BL$6;($BL$6-Q56)*$DU$6*$BP$6/$G$6;0)"""
    # dT = TSD.Tdhc[t] - M.
    # if
    pass


if __name__ == "__main__":

# generate model

## load PEExcel "SIM" Inputs
    from pyped.excel import load_inputs_from_PEExcel
    M = pyped.datamodel.PED.from_PEExcel("../data/PlusenergieExcel_Performance.xlsb")

## load Timeseries Data
    TSD = pyped.datamodel.TimeSeriesData(months=np.genfromtxt("../data/profiles/months.csv"))
## load climate data
    TSD.TA = np.genfromtxt("../data/profiles/climate.csv",
                           delimiter=";")[1:, 1]
## load solar gains
    TSD.QS = np.genfromtxt("../data/profiles/QS_test.csv")  # W/m²

## load Nutzungsprofile: PEExcel "Energiesumme"
    Usage = pd.read_csv("../data/profiles/usage_profiles.csv", encoding="cp1252")

## load usage profiles
    TSD.QI = Usage["Qi Sommer W/m²"].to_numpy()
    TSD.ACH_V = Usage["Luftwechsel_Anlage_1_h"].to_numpy()
    TSD.ACH_I = Usage["Luftwechsel_Infiltration_1_h"].to_numpy()
    TSD.Qdhw = Usage["Warmwasserbedarf_W_m2"].to_numpy()


# Simulate
    TSD = simulate(M, TSD)


# Plot
    # pyped.Plot.plot_Temp_Q(TSD.TI, TSD.TA,
    #                        TSD.QT, TSD.QV, TSD.QS, TSD.QI, TSD.Qh_min, TSD.Qc_min, TSD.ACH_V

    if input("plot results?") == "y":
        import pyped.Plot as ppp

        fig = ppp.plot_Qx(*TSD.list_qx(), start=1, end=8760)
        ppp.show_figure(fig)


    if input("save TSD?") == "y":
        path = "../data/sim/"+input("save Excel to ../data/sim/", )
        TSD.to_excel(path=path)

# Dashboard
    if input("load dashboard?") == "y":
        import pyped.dasboard

        d = pyped.dasboard.Dashboard(TSD, M)
