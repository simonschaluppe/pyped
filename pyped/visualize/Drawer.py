import random
from tkinter import *
from pyped.visualize.Canvas import cCanvas

def draw_building(canvas:cCanvas, storeys=6, xaw=12, gh=3.5):
    # all storeys

    storey_dict = {}

    for storey in range(-1, storeys):
        draw_storey_part(canvas, number=storey, x_end=xaw, gh=gh)
        storey_dict[f"{storey}. Stock"] = {"x0": 0}
    # has usages [BGF]

    storey_dict = {}

    # draw roof
    draw_PV_roof(canvas)
    draw_PV_facade(canvas)

    canvas.create_line(0, 0, xaw, 0, arrow=LAST, fill="white", width=2)
    canvas.create_text(xaw / 2, -1.5, text=f"Trakttiefe {xaw} m", fill="white")


def draw_storey_part(canvas:cCanvas, number, x_end, gh, x0=0):
    x0 = x0
    y0 = 0 + number
    x1 = x_end
    y1 = 1 + number
    canvas.create_rectangle(x0, y0, x1, y1, fill="darkgrey")
    canvas.create_line(x0, y0, x0, y1 + 0.1, arrow=NONE, fill="#BE81F7", width=5)
    canvas.create_line(x1, y0, x1, y1 + 0.1, arrow=NONE, fill="#BE81F7", width=5)
    canvas.create_text(x1 / 2, 0.5 * (y0 + y1), text=f"storey {number}")
    canvas.create_text(x0 - 2, 0.5 * (y0 + y1), text=f"{gh} m")


def draw_PV_roof(canvas:cCanvas, total_storeys=6, xaw=12,pv_roof_coverage_pct=0.6, spacing=1.5):
    dx_i = 1 + spacing
    n = round(xaw * pv_roof_coverage_pct / dx_i)

    for row in range(n):
        x0 = 0 + row * dx_i + 0.5
        y0 = total_storeys
        x1 = x0 + 1
        dy = 0.2
        canvas.create_line(x0, y0, x1, y0 + dy, arrow=NONE, fill="darkblue", width=3)
        canvas.create_line(x0 + 1, y0 + dy, x1 + 1, y0, arrow=NONE, fill="darkblue", width=3)


def draw_PV_facade(canvas:cCanvas, total_storeys=6, xaw=12, fenestration=0.4, storeys=3):
    for storey in range(total_storeys, total_storeys - storeys, -1):
        canvas.create_line(xaw + 0.1, storey + 0.1, xaw + 0.6, storey + 0.1 - fenestration,
                           arrow=NONE, fill="darkblue", width=3)


def draw_plot(canvas:cCanvas):
    # dirt beneath
    # canvas.create_rectangle(-5, 0, 30, -10, fill="darkgreen", line=None)
    canvas.create_rectangle(-5, -0.1, 30, -10, fill="#29220A", line=None)
    # sky
    # canvas.create_rectangle(-5, 0, 30, 20, fill="lightblue", line=None)
    for i in range(-5, 30):
        dh = 0.03 + 0.1 * (random.random())
        canvas.create_rectangle(i, -0.1, i + 1, dh, outline="green", fill="green", width=0, line=None)
    # green line


def draw_boreholes(canvas:cCanvas, number):
    for i in range(number):
        canvas.create_rectangle(8 + i, -1, 8.4 + i, -10, fill="brown", outline="grey", width=2)


def draw_axis(canvas:cCanvas):
    canvas.create_line(0, 0, 1, 0, arrow=LAST, fill="blue")
    canvas.create_line(0, 0, 0, 1, arrow=LAST, fill="blue")


def draw_info(canvas:cCanvas, lines: list):
    lineheight = 1
    y = 7
    for i, line in enumerate(lines):
        canvas.create_text(20, y + lineheight * i, text=line, fill="white",
                           font="12pt")

def draw(canvas:cCanvas, data:dict):
    draw_plot(canvas)
    draw_building(canvas, data)
    draw_boreholes(canvas, 4)
    draw_axis(canvas)
    draw_info(canvas, ["Testgebäude", "BGF: "])


def _demo_PED2D():

    fenster = Tk()
    fenster.geometry("700x800")
    ebene = cCanvas(fenster, ox=80, oy=600, ex=20, ey=50, width=1000, height=900)
    ebene.pack()

    draw(ebene, data)
    fenster.mainloop()


if __name__ == "__main__":

    import pyped.excel_utils.utils as pex
    data = pex.read("../data/clean/Clean_testped2.xlsx")
