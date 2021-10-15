

from tkinter import *

class Model:
    pv_roof_coverage_pct = 0.6
    xaw=12
    storeys=6
    pv_facade_storeys = 3
    fenestration_pct=0.4

class cCanvas(Canvas):
    """comments-bereich"""

    def __init__(self,master=None,ox=100,oy=100,ex=15,ey=15,width=200,height=200, bg="white"):

        self.ox=ox
        self.oy=oy
        self.ex=ex
        self.ey=ey
        
        Canvas.__init__(self,master)
        
        self["width"]=width
        self["height"]=height
        self["bg"]=bg
        


        
    def cx(self, x):
        return self.ox + x*self.ex
    
    
    def cy(self, y):
        return self.oy - y*self.ey

    def umrechnen(self, xyTupel):
        n=len(xyTupel)
        liste=[]
        for i in range(n):
            if i%2==0:
                xy_alt=self.cx(xyTupel[i])
            else:
                xy_alt=self.cy(xyTupel[i])
            liste+=[xy_alt]
        return tuple(liste)
        
    def create_line(self, *coords, **opts):
        coords_alt=self.umrechnen(coords)
        return Canvas.create_line(self, *coords_alt, **opts)

    def create_oval(self, *coords, **opts):
        coords_alt=self.umrechnen(coords)
        return Canvas.create_oval(self, *coords_alt, **opts)

    def create_rectangle(self, *coords, **opts):
        coords_alt=self.umrechnen(coords)
        return Canvas.create_rectangle(self, *coords_alt, **opts)

    def create_polygon(self, *coords, **opts):
        coords_alt=self.umrechnen(coords)
        return Canvas.create_polygon(self, *coords_alt, **opts)

    def create_text(self, *coords, **opts):
        coords_alt=self.umrechnen(coords)
        return Canvas.create_text(self, *coords_alt, **opts)



def _demo():
    fenster=Tk()
    fenster.geometry("400x300")
    ebene=cCanvas(fenster)
    ebene.pack()
    ebene.create_line(-4,0,4,0,arrow=LAST, fill="blue")
    fenster.mainloop()



if __name__ == '__main__':
    _demo()



        
