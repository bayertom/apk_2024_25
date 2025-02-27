from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *

class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__q = QPointF(0.0, 0.0)
        self.__pol = QPolygonF()
        

    def mousePressEvent(self, e:QMouseEvent):
        
        #Get coordinates x,y
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPointF(x, y)
        
        #Add to point to polygon
        self.__pol.append(p)
        
        #Repaint screen
        self.repaint()
 
 
    def paintEvent(self, e: QPaintEvent):
        #Create new graphic object
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
      
        #Set graphic attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw objects
        qp.drawPolygon(self.__pol)
        
        #End drawing
        qp.end()