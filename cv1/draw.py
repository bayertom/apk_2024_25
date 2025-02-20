from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *

class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__q = QPointF(0.0, 0.0)
        self.__pol = QPolygonF()
        

    def mousePressEvent(self, e):
        
        #Get coordinates x,y
        
        #Create new point
        
        #Add to point to polygon
        
        #Repaint screen
        
        pass