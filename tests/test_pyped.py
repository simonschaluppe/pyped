import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest

import pyped.read


def test_read():
    test_meta = pyped.read.Meta.from_xlsx("data/META_name_value.xlsx")
    assert test_meta.building_floor_area.value == 4034.625

    assert test_meta.auxiliary_power_percentage_district_heating.excel_name     == 'Hilfsstromanteil Gasheizung/Fernwärme'
    assert test_meta.auxiliary_power_percentage_district_heating.header_range   == 'META!$BX$2'
    assert test_meta.auxiliary_power_percentage_district_heating.value_range    == 'META!$BX$3'
    assert test_meta.auxiliary_power_percentage_district_heating.value          == 0.05