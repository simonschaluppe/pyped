
import xlwings as xw
from collections import defaultdict
from dataclasses import dataclass, field, fields, MISSING


# we want an Object that represents a PEExcel and gives access to its inputs
# the object should provide different methods of obtaining the various values, inputs at first
# get_by_PEExcel_header_name
# get_by_named_range

@dataclass
class PEECell:
    """
    Eine Zelle im PEEExcel

    """
    category: str
    description: str
    desc_address: str

    value: float


class PEExcel:
    """
    attributes .python_name = PEEce- Value:
    """

    def __init__(self, path_to_PEExcel):

        wb = xw.Book(path_to_PEExcel)

        names = wb.names["sim_input_names"].refers_to_range  # xW Range object
        vals = wb.names["sim_input_vals"].refers_to_range  # xW Range object
        pyvars = wb.names["sim_input_python_var_names"].refers_to_range  # xW Range object
        cats = names.offset(-1,0)
        self.inputs = defaultdict()

        for cat_r, name_r, val_r in zip(cats, names, vals):
            address = val_r.sheet.name + "!" + val_r.address
            self.inputs[name_r.value] = PEECell(category=cat_r.value,
                                       desc_address=address,
                                       description=name_r.value,
                                       value=val_r.value)


def load_inputs_from_PEExcel(path_to_PEExcel):
    """

    :param path_to_PEExcel:
    :return: sim_inputs: dict[PEExcel Name] = PEExcel Value
    """
    sim_inputs = defaultdict()

    wb = xw.Book(path_to_PEExcel)

    name = wb.names["sim_input_names"].refers_to_range  # xW Range object
    vals = wb.names["sim_input_vals"].refers_to_range  # xW Range object

    for val, name in zip(vals, name):
        sim_inputs[name.value] = val.value

    return sim_inputs


if __name__ == "__main__":
    default_path = "data/PlusenergieExcel_Performance.xlsb"
    tPEE = PEExcel(default_path)
    tinputs = load_inputs_from_PEExcel(default_path)



