
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

class meta():
    def __init__(self):
        self.Summe_NGF = excel_read("Summe_NGF")



def (WWt, Qt,StrombedarfausBatterie ):
    meta.Summe_NGF