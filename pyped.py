#
# import pyped.read
# TA = pyped.read.Profile.read_climate("data/profiles/climate.csv") ## relative path from here
#


import numpy as np
import pandas as pd
import pyped.datamodel, pyped.Plot, pyped.simulation
from pyped.excelLoader import load_inputs_from_PEExcel

########### generate model

#### PEExcel "Sim"
SI = load_inputs_from_PEExcel("data/PlusenergieExcel_Performance.xlsb")
M = pyped.datamodel.Model(SI)

#### Timeseries Data
TSD = pyped.datamodel.TimeSeriesData()
# climate data
TSD.TA = np.genfromtxt("data/profiles/climate.csv",
                       delimiter=";")[1:, 1]
# solar gains
TSD.QS = np.genfromtxt("data/profiles/QS_test.csv")  # W/m²

# Nutzungsprofile: PEExcel "Energiesumme"
Usage = pd.read_csv("data/profiles/usage_profiles.csv", encoding="cp1252")
# usage profiles
TSD.QI = Usage["Qi Sommer W/m²"].to_numpy()
TSD.ACH_V = Usage["Luftwechsel_Anlage_1_h"].to_numpy()
TSD.ACH_I = Usage["Luftwechsel_Infiltration_1_h"].to_numpy()
TSD.Qdhw = Usage["Warmwasserbedarf_W_m2"].to_numpy()


########### Simulate




def simulate(M: pyped.datamodel.Model, TSD: pyped.datamodel.TimeSeriesData):
    cI = M.cI  # speicherkapazität
    TI_min = M.heat.minimum_room_temperature
    TI_max = M.cool.minimum_room_temperature
    TSD.TI[0] = TI_min

    for t in range(1, 8760):

        calc_QV(M, TSD, t)
        ##
        calc_QT(M, TSD, t)

        Q_sum = (TSD.QT[t] + TSD.QV[t]) + TSD.QS[t] + TSD.QI[t]
        TSD.TI[t] = TSD.TI[t - 1] + Q_sum / M.cI
        TI_min = M.heat.minimum_room_temperature
        TI_max = M.cool.minimum_room_temperature

        if TSD.TI[t] < TI_min and is_heating_season(M, TSD, t):
            TSD.Qh_min[t] = (TI_min - TSD.TI[t]) * M.cI
            # TSD.TI[t] = TSD.TI[t] + TSD.Qh[t] / M.cI
            TSD.TI[t] = TI_min

        if TSD.TI[t] > TI_max and is_cooling_season(M, TSD, t):
            TSD.Qc_min[t] = (TI_max - TSD.TI[t]) * M.cI
            # TSD.TI[t] = TSD.TI[t] + TSD.Qc[t] / M.cI
            TSD.TI[t] = TI_max

        calc_DHW(M, TSD, t)


# plt.plot(TA)

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
    room_height = M.size.rh
    cp_air = M.const.cp_air

    # thermally effective air change

    if M.vent.use_heat_recovery:
        if is_heating_season(M, TSD, t):
            # heat recovery
            eff_share_after_heat_recovery = 1 - M.vent.hr_w  # relative to unrecovered
        elif is_cooling_season(M, TSD, t):
            # cool recovery
            eff_share_after_heat_recovery = 1 - M.vent.cr_s  # relative to unrecovered
        else:
            # heat recovery
            eff_share_after_heat_recovery = 1 - M.vent.cr_s  # relative to unrecovered
    else:
        rel_ACH_after_heat_recovery = 1  # relative to unrecovered
    eff_airchange = TSD.ACH_I[t] \
                    + TSD.ACH_V[t] * M.vent.share_cs \
                    + TSD.ACH_V[t] * (1 - M.vent.share_cs) * rel_ACH_after_heat_recovery

    QV = eff_airchange * room_height * cp_air * dT
    TSD.QV[t] = QV
    return


def calc_QT(M, TSD, t):
    dT = TSD.TA[t - 1] - TSD.TI[t - 1]
    QT = M.hull.QT_dT * dT
    TSD.QT[t] = QT
    return

def calc_DHW(M, TSD, t):
    """=WENN(Q56<$BL$6;($BL$6-Q56)*$DU$6*$BP$6/$G$6;0)"""
    # dT = TSD.Tdhc[t] - M.
    # if
    pass

def test():
    simulate(M, TSD)
    pyped.Plot.plot_Temp_Q(TSD.TI, TSD.TA,
                           TSD.QT, TSD.QV, TSD.QS, TSD.QI, TSD.Qh_min, TSD.Qc_min, TSD.ACH_V)


if __name__ == "__main__":
    test()
