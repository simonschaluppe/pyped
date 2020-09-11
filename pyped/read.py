
import openpyxl
import xlwings as xw
import pdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    def from_xlsx(cls ,path):
        """
        reads excel from path and returns dict of named ranges
        :param path:
        :return: dict {name: {excel_name, header_range, value_range, value}}:
        """

        wb = xw.Book(path)
        meta = {}

        for name in wb.names:
            # TODO: Check for first qualifier ("meta_"), or rename class in "Inputs" or smth?
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


class Profile:

    def __init__(self, df, unit):
        self.df = df
        self.name = self.df.name
        self.unit = unit
        self.dt = 8760 / len(df[:]) # hours

    def plot_OALC(self):
        """Plots the Ordered Annual Load Curve of the Profile"""
        self.df.plot()

        fig, ax = plt.subplots(1, 1, figsize=(15, 6))
        self.df.sort_values(ascending=False) \
                .reset_index(drop=True)\
                .plot();
        plt.show()


    @classmethod
    def read_wind(cls, path="../data/profiles/wind.csv"):
        df = pd.read_csv(path,
                         delimiter=";",
                         index_col="H")
        # first profile:
        profile = df[df.columns[0]]

        return cls(profile, "MW")

if __name__ == "__main__":

    # meta_cls = Meta.from_xlsx("../data/META_name_value.xlsx")

    wind = Profile.read_wind()
    wind.df.plot()
