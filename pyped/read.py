

import openpyxl
import xlwings as xw
import pdb



class Meta:

    def __init__(self, meta_names):
        self.__dict__ = meta_names

    @classmethod
    def from_xlsx(cls, path):
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        rng = wb.defined_names
        meta_names_dict = {}
        for name in wb.defined_names.definedName:

            # print(f"{name.name} @ {name.value}")
            sheet, coords = name.value.split("!")
            # print(wb[sheet][coords].value)
            name = name.name.replace("meta_", "")
            coords = coords.replace("2", "3")
            meta_names_dict[name] = wb[sheet][coords].value

        return cls(meta_names_dict)
        # print(META)


def from_xlsx(path):
    """
    reads excel from path and returns dict of named ranges
    :param path:
    :return: dict {name: {range, value}}:
    """

    # TODO: sollte ein Meta() obejct bauen, das den namen in excel speichert, und aber auch den value EINE ZEILE weiter unten
    wb = xw.Book(path)
    meta = {}

    for name in wb.names:
        meta[name.name] = {"range": name.refers_to_range, "value": name.refers_to_range.value}

    print(meta)
    print(f"META loaded from {path}")
    return meta
    #

print(__name__)

if __name__ == "__main__":

    # meta = from_xlsx("data/META.xlsx")
    # meta_cls = Meta(meta)
    # meta["meta_building_floor_area"]["value"]

    meta_cls2 = Meta.from_xlsx("../data/META.xlsx")
    # pdb.set_trace()
