
import openpyxl

wb = openpyxl.load_workbook("data/test.xlsx", read_only=True)
rng = wb.defined_names["META_input"]
dests = rng.destinations

for title, coord in dests:
    ws = wb[title]
    cells= ws[coord]

META = {}
for col in range(len(cells[0])):
    META[cells[0][col].value] = cells[1][col].value


print(META)

class Meta():

    def __init__(self, meta_names):
        self.names = meta_names

import xlwings as xw

def from_xlsx(path):
    """
    reads excel from path and returns dict of named ranges
    :param path:
    :return: dict {name: {range, value}}:
    """
    wb = xw.Book(path)
    meta = {}
    for name in wb.names:
        meta[name.name] = {"range": name.refers_to_range, "value": name.refers_to_range.value}
    # %%
    wb.close()
    print("META loaded from {path}")
    return meta
    #

print(__name__)

if __name__ == "__main__":
    meta = from_xlsx("data/META.xlsx")

    meta_cls = Meta(meta)
    meta["meta_building_floor_area"]["value"]
    pdb.set_trace()