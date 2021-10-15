
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
import bokeh.plotting as bpl
from bokeh.models import ColumnDataSource, LabelSet


class Dashboard(param.Parameterized):


    hour                    = param.Range(default=(1, 72), bounds=(1, 8760))
    # boolean                 = param.Boolean(True, doc="A sample Boolean parameter")
    # color                   = param.Color(default='#FFFFFF')
    # date                    = param.Date(dt.datetime(2017, 1, 1),
    #                                      bounds=(dt.datetime(2017, 1, 1), dt.datetime(2017, 2, 1)))

    tsd_df                  = param.DataFrame(pd.util.testing.makeDataFrame().iloc[:3])
    # select_string           = param.ObjectSelector(default="yellow", objects=["red", "yellow", "green"])
    # select_fn               = param.ObjectSelector(default=list, objects=[list, set, dict])
    # int_list                = param.ListSelector(default=[3, 5], objects=[1, 3, 5, 7, 9], precedence=0.5)
    # single_file             = param.FileSelector(path='../../*/*.py*', precedence=0.5)
    # multiple_files          = param.MultiFileSelector(path='../../*/*.py?', precedence=0.5)

    # timestamps = []
    # record_timestamp        = param.Action(lambda x: x.timestamps.append(dt.datetime.utcnow()),
    #                                        doc="""Record timestamp.""", precedence=0.7)

    def __init__(self, TSD:pyped.datamodel.TimeSeriesData, M:pyped.datamodel.PED, **params):
        super().__init__(**params)
        self.TSD = TSD
        self.M = M
        self.tsd_df = self.TSD.as_df()
        self.dataframe = pn.widgets.DataFrame(self.tsd_df, height=400, widths=150, frozen_columns=1, autosize_mode='fit_columns')


        q = self.i_heat_balance
        t = self.i_temperature

    # col1
#
        source = ColumnDataSource(self.tsd_df)

        p = bpl.figure(plot_height=350, title="Wärmebilanz",
                       tools="hover,pan,reset,save,box_zoom",
                       x_range=[1, 8760], y_range=[-50., 50.]) #tooltips="@country: @value"

        r = p.line(x="index", y="QT",source=source, legend_label="Transmissionswärme", color="#ff4400")
        r = p.line(x="index", y="QV",source=source, legend_label="Lüftungswärmeverluste", color="#0055FF")
        r = p.line(x="index", y="QS",source=source, legend_label="Solare Wärmegewinne", color="#ffee00")
        r = p.line(x="index", y="QI",source=source, legend_label="Interne Wärmegewinne", color="#FF0000")
        r = p.line(x="index", y="Qh_min",source=source, legend_label="Heizung", color="#ff4400")
        r = p.line(x="index", y="Qc_min",source=source, legend_label="Kühlung", color="#00DDFF")
        p.yaxis.axis_label = 'Wärmestrom [W/m²NGF]'

        Qx = pn.pane.Bokeh(p)

        gf = 7330.0
        depth = np.sqrt(gf)

        bebfl = gf * self.M.Plot.density
        geschosse = self.M.Plot.net_floor_area / bebfl
        d = self.M.Plot.net_storey_height
        h = d * geschosse

        x = bebfl / depth
        y = gf / depth


        source = ColumnDataSource(data=dict(bottom=[0], top=[h],
                                            left=[d], right=[d + x],
                                            names=["PED"],
                                            bebfl=[bebfl]))
        TOOLTIPS = [
            ("names", "@names"),
            ("bebfl", "$bebfl"),
        ]
        p = bpl.figure(plot_height=350, title="PED 2D Visualization",
                       tools="hover,pan,reset,save,box_zoom",
                       x_range=[0, y + 2 * d], y_range=[-2 * d, h + d],
                       tooltips=TOOLTIPS)

        # p.quad(bottom=[0], left=[d],top=[h], right=[d+x], color="#B3DE69")



        p.quad(source=source, color="#B3DE69")
        labels = LabelSet(x='top', y='right', text='names', level='glyph',
                          x_offset=15, y_offset=15, source=source, render_mode='canvas')
        p.add_layout(labels)
        # r = p.line(x="index", y="QT",source=source, legend_label="Transmissionswärme", color="#ff4400")
        # r = p.line(x="index", y="QV",source=source, legend_label="Lüftungswärmeverluste", color="#0055FF")
        # r = p.line(x="index", y="QS",source=source, legend_label="Solare Wärmegewinne", color="#ffee00")
        # r = p.line(x="index", y="QI",source=source, legend_label="Interne Wärmegewinne", color="#FF0000")
        # r = p.line(x="index", y="Qh_min",source=source, legend_label="Heizung", color="#ff4400")
        # r = p.line(x="index", y="Qc_min",source=source, legend_label="Kühlung", color="#00DDFF")
        p.yaxis.axis_label = 'Höhe [m]'
        p.xaxis.axis_label = 'Quartierslänge [m]'

        ped_2d = pn.pane.Bokeh(p)
#


        self.col1 = pn.Column(Qx, ped_2d)


    #col2
        self.input_props = {}
        for prop, val in self.M.PEE_inputs.items():
            w = pn.widgets.TextInput(name=str(prop), placeholder=str(val))
            self.input_props[prop] = w

        self.PEE_card = pn.Card(*self.input_props.values(), title="PlusenergieExcel Inputs", background="WhiteSmoke", collapsed=True)

        self.Plot_props = []
        for name, cat in self.M.Plot.__dict__.items():
            w = pn.widgets.TextInput(name=str(name) + ":", placeholder=str(cat))
            self.Plot_props.append(w)

        self.Plot_card = pn.Card(*self.Plot_props, title="Plot", background="WhiteSmoke", collapsed=True)


        self.col2 = pn.Column(self.PEE_card,self.Plot_card)

    #col3
        self.col3 = pn.Column(self.dataframe.round())

        self.dash = pn.Row(self.col1, self.col2, self.col3).show(threaded=True)

    def heat_balance(self, start=1, end=8760, view_fn=ppp.plot_Qx):
        return view_fn(*self.TSD.list_qx(), start=start, end=end)

    @param.depends("hour")
    def i_heat_balance(self):
        start, end = self.hour
        return self.heat_balance(start=start, end=end)

    @param.depends("hour")
    def i_temperature(self):
        start, end = self.hour
        return ppp.plot_Temp(self.TSD.TI, self.TSD.TA, start=start,end=end)


if __name__ == "__main__":
    from pyped.excel import load_inputs_from_PEExcel
    from pyped.datamodel import PED

    test_model = PED.from_PEExcel("../data/PlusenergieExcel_Performance.xlsb")

    tsd_test = pyped.datamodel.TimeSeriesData(months= np.genfromtxt("../data/profiles/months.csv"))
    tsd_test.load_csv("../data/test/TSD_test.csv")
    dash_test = Dashboard(TSD=tsd_test, M=test_model)
