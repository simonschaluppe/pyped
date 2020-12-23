
#
# import pyped.read
# TA = pyped.read.Profile.read_climate("data/profiles/climate.csv") ## relative path from here
#

import pandas as pd

import numpy as np


TA  = pd.read_csv("data/profiles/climate.csv",
    delimiter=";",
    index_col="H").to_numpy()

QS = 9.95 * np.ones((8760,1))
QI = 4.76 * np.ones((8760,1))

for t in range(0, 8760):
    print(t, TA[t], QS[t], TA[t]+QS[t])

