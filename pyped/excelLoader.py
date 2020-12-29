

import xlwings as xw
from collections import defaultdict


class PEECell():
    """
    Eine Zelle im PEEExcel

    """
    def __init__(self, description: xw.Range, value: xw.Range):
        self.description_range = description
        self.value_range = value
        self.value = self.value_range.value

    def __repr__(self):
        return self.description_range.value

    def __add__(self, other):
        return self.value + other


# class PEExcel_SimInput():
#     """
#     attributes .python_name = PEEce- Value:
#     """
#     #net_room_height: float = 2.5
#
#     def __init__(self, path_to_PEExcel):
#         sim_inputs = defaultdict()
#
#         wb = xw.Book(path_to_PEExcel)
#
#         descriptions = wb.names["sim_input_names"].refers_to_range  # xW Range object
#         vals = wb.names["sim_input_vals"].refers_to_range  # xW Range object
#         pyvars = wb.names["sim_input_python_var_names"].refers_to_range  # xW Range object
#
#         for pyvar, val in zip(pyvars, vals):
#             self.__dict__[str(pyvar.value)] = val.value

def load_inputs_from_PEExcel(path_to_PEExcel):
    """

    :param path_to_PEExcel:
    :return: sim_inputs: dict[PEExcel Name] = PEExcel Value
    """
    sim_inputs = defaultdict()

    wb = xw.Book(path_to_PEExcel)

    name = wb.names["sim_input_names"].refers_to_range     #xW Range object
    vals = wb.names["sim_input_vals"].refers_to_range    #xW Range object

    for val, name in zip(vals, name):
        sim_inputs[name.value] = val.value

    return sim_inputs


if __name__ == "__main__":
    default_path = "data/PlusenergieExcel_Performance.xlsb"
    test_si = PEExcel_SimInput(default_path)
    test_inputs = load_inputs_from_PEExcel(default_path)



