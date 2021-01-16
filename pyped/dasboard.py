
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import panel as pn
import panel.widgets as pnw
from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvas

import pyped.Plot as ppp
import pyped.datamodel
import param
import datetime as dt



class Dashboard(param.Parameterized):

    timestamps = []

    hour                    = param.Range(default=(1, 72), bounds=(1, 8760))
    boolean                 = param.Boolean(True, doc="A sample Boolean parameter")
    color                   = param.Color(default='#FFFFFF')
    date                    = param.Date(dt.datetime(2017, 1, 1),
                                         bounds=(dt.datetime(2017, 1, 1), dt.datetime(2017, 2, 1)))
    dataframe               = param.DataFrame(pd.util.testing.makeDataFrame().iloc[:3])
    select_string           = param.ObjectSelector(default="yellow", objects=["red", "yellow", "green"])
    select_fn               = param.ObjectSelector(default=list,objects=[list, set, dict])
    int_list                = param.ListSelector(default=[3, 5], objects=[1, 3, 5, 7, 9], precedence=0.5)
    single_file             = param.FileSelector(path='../../*/*.py*', precedence=0.5)
    multiple_files          = param.MultiFileSelector(path='../../*/*.py?', precedence=0.5)
    record_timestamp        = param.Action(lambda x: x.timestamps.append(dt.datetime.utcnow()),
                                           doc="""Record timestamp.""", precedence=0.7)

    def __init__(self, TSD, **params):
        super().__init__(**params)
        self.TSD = TSD

        self.col = pn.Row(self.param)

        self.dash = pn.Row(self.col,self.i_heat_balance,).show(threaded=True)

    def heat_balance(self, start=1, end=8760, view_fn=ppp.plot_Qx):
        return view_fn(*self.TSD.list_qx(), start=start, end=end)

    @param.depends("hour")
    def i_heat_balance(self):
        start, end = self.hour
        return self.heat_balance(start=start, end=end)

    def temperature(self, variable="Qh", start=1, end=8759, view_fn=ppp.plot_Temp):
        return view_fn(self.TSD.TI,self.TSD.TA)


if __name__ == "__main__":

    tsd_test = pyped.datamodel.TimeSeriesData(months= np.genfromtxt("../data/profiles/months.csv"))
    tsd_test.load_csv("../data/test/TSD_test.csv")
    dash_test = Dashboard(TSD=tsd_test)
