

import xlwings as xw
from collections import defaultdict

# meta_cls = Meta.from_xlsx("../data/META_name_value.xlsx")
# EXCEL_PATH = "../data/PlusenergieExcel_Performance.xlsb"
# wb = xw.Book(EXCEL_PATH)
# meta = {}

def load_inputs_from_PEExcel(path_to_PEExcel):
    sim_inputs = defaultdict()

    wb = xw.Book(path_to_PEExcel)

    names = wb.names["sim_input_names"].refers_to_range     #xW Range object
    vals  = wb.names["sim_input_direkt"].refers_to_range    #xW Range object

    for name, val in zip(names, vals):
        sim_inputs[name.value] = val.value

    return sim_inputs


if __name__ == "__main__":
    default_path = "data/PlusenergieExcel_Performance.xlsb"

    test_inputs = load_inputs_from_PEExcel(default_path)

