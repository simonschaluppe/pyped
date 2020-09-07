

import openpyxl
import xlwings as xw
import pdb

class Property:
    def __init__(self, attributes):
        self.__dict__ = attributes

class Meta:

    def __init__(self, properties):
        self.__dict__ = properties

    # @classmethod
    # def from_xlsx2(cls, path):
    #     """ only gives name and value separately"""
    #     wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    #     rng = wb.defined_names
    #     meta_names_dict = {}
    #     for name in wb.defined_names.definedName:
    #         # print(f"{name.name} @ {name.value}")
    #         sheet, coords = name.value.split("!")
    #         # print(wb[sheet][coords].value)
    #         name = name.name.replace("meta_", "")
    #         #coords = coords.replace("2", "2")
    #         meta_names_dict[name] = wb[sheet][coords].value
    #
    #     return cls(meta_names_dict)
    #     # print(META)

    @classmethod
    def from_xlsx(cls,path):
        """
        reads excel from path and returns dict of named ranges
        :param path:
        :return: dict {name: {excel_name, header_range, value_range, value}}:
        """

        wb = xw.Book(path)
        meta = {}

        for name in wb.names:
            # name or value?
            real_name = name.name.replace("meta_", "").replace("_name", "").replace("_value", "")
            if name.name.endswith("_name"):
                data = {"excel_name": name.refers_to_range.value,
                        "header_range": "!".join([name.refers_to_range.sheet.name, name.refers_to_range.address])}
            if name.name.endswith("_value"):
                data = {"value_range": "!".join([name.refers_to_range.sheet.name, name.refers_to_range.address]),
                        "value": name.refers_to_range.value}
            if real_name in meta.keys():
                meta[real_name].__dict__.update(data)
            else:
                meta[real_name] = Property(data)

        return cls(meta)

if __name__ == "__main__":

    meta_cls = Meta.from_xlsx("../data/META_name_value.xlsx")
    # pdb.set_trace()
