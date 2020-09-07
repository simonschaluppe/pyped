import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import pyped.read


def test_read():
    test_meta = pyped.read.Meta.from_xlsx("data/META.xlsx")
    assert test_meta.building_floor_area is not None
