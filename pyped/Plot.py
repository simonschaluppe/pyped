import matplotlib.pyplot as plt
import numpy as np


def plot_Temp_Q(
        TI:np.ndarray    = np.zeros(8760),
        TA:np.ndarray    = np.zeros(8760),
        QT:np.ndarray    = np.zeros(8760),
        QV:np.ndarray    = np.zeros(8760),
        QS:np.ndarray    = np.zeros(8760),
        QI:np.ndarray    = np.zeros(8760),
        Qh:np.ndarray    = np.zeros(8760),
        Qc:np.ndarray    = np.zeros(8760),
        QV_dT:np.ndarray = np.zeros(8760)
        ):

    fig, ax = plt.subplots(3 ,1 ,figsize=(5 ,10))
    ax[0].plot(TI)
    ax[0].plot(TA)
    ax[0].legend(["TI" ,"TA"])

    ax[1].plot(QT)
    ax[1].plot(QV)
    ax[1].plot(QS)
    ax[1].plot(QI)
    ax[1].plot(Qh)
    ax[1].plot(Qc)
    ax[1].set_ylim(-50,50)
    ax[1].legend(["QT" ,"QV" ,"QS" ,"QI", "Qh" ,"Qc"])

    ax[2].plot(QI[:72])
    ax[2].plot(QV_dT[:72])
    ax[2].set_yscale('log')        # because different units, dimensions etc
    ax[2].legend(["QI" ,"QV_dT"])

    fig.show()
