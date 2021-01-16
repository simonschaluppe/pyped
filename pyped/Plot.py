import matplotlib.pyplot as plt
from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvas
import numpy as np


def mpl_plot(avg, highlight):
    fig = Figure()
    # FigureCanvas(fig) # not needed in mpl >= 3.1
    ax = fig.add_subplot()
    ax.plot(avg)
    if len(highlight): highlight.plot(style='o', ax=ax)
    return fig

def plot_df(df):
    fig = Figure()
    # FigureCanvas(fig) # not needed in mpl >= 3.1
    ax = fig.add_subplot()
    ax.plot(df)
    return fig

def plot_Qx(QT:np.ndarray    = np.zeros(8760),
        QV:np.ndarray    = np.zeros(8760),
        QS:np.ndarray    = np.zeros(8760),
        QI:np.ndarray    = np.zeros(8760),
        Qh:np.ndarray    = np.zeros(8760),
        Qc:np.ndarray    = np.zeros(8760)):
    fig = Figure()
    # FigureCanvas(fig)  # not needed in mpl >= 3.1
    ax = fig.add_subplot()
    ax.plot(QT)
    ax.plot(QV)
    ax.plot(QS)
    ax.plot(QI)
    ax.plot(Qh)
    ax.plot(Qc)
    ax.set_ylim(-50,50)
    ax.legend(["QT" ,"QV" ,"QS" ,"QI", "Qh" ,"Qc"])
    return fig

def plot_Temp(
        TI:np.ndarray    = np.zeros(8760),
        TA:np.ndarray    = np.zeros(8760),):

    fig, ax = plt.subplots()
    ax.plot(TI)
    ax.plot(TA)
    ax.legend(["TI", "TA"])
    return fig

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



if __name__ == "__main__":
    print("nothing to do")


    #  interactive sankey code snippers
    #  this to dashboard?
    # from ipysankeywidget import SankeyWidget
    #
    #
    #
    # from ipywidgets import (
    #     VBox,
    #     HBox,
    #     IntSlider,
    # # )
    #
    #
    # def slider(link, i, sankey):
    #     value = IntSlider(description="{source} → {target}".format(**link), min=0, max=10, step=1, value=10)
    #
    #     def _change(change):
    #         sankey.links[i]["value"] = value.value
    #         sankey.send_state()
    #
    # #     value.observe(_change)
    #
    #     return value
    # links = [
    #     {'source': 'start', 'target': 'A', 'value': 10},
    #     {'source': 'A', 'target': 'B', 'value': 10},
    #     {'source': 'C', 'target': 'A', 'value': 10},
    #     {'source': 'A', 'target': 'C', 'value': 10},
    # ]
    #
    # sankey = SankeyWidget(links=links)
    #
    #
    # sliders = [slider(link, i, sankey) for i, link in enumerate(links)]
    #
    # box = HBox(children=[sankey, VBox(children=sliders)])
