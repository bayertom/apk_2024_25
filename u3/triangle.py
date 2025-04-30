from qpoint3df import*
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Triangle:
    def __init__ (self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF, slope_:float, aspect_:float):
        #Triangle of DTM
        self.vertices = QPolygonF()
        self.vertices.append(p1)
        self.vertices.append(p2)
        self.vertices.append(p3)
        self.slope = slope_
        self.aspect = aspect_
        
    def getVertices(self):
        #Get triangle vertices
        return self.vertices
    
    def getSlope(self):
        #Get triangle slope
        return self.slope
    
    def getAspect(self):
         #Get triangle aspect
        return self.aspect