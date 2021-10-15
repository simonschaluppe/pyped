import xlwings as xw
import pandas as pd
from collections import defaultdict

def read(filepath):
    d = dict()
    b = xw.Book(filepath)

    for s in b.sheets:
        d[s.name] = {}
        for t in s.tables:
        for row in t.data_body_range:
            d[s.name][row[0].value] = row[1].value

    return d
