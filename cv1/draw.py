from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *

class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__q = QPointF(0.0, 0.0)
        self.__pol = QPolygonF()
        self.__add_vertex = False
        

    def mousePressEvent(self, e:QMouseEvent):
        
        #Get coordinates x,y
        x = e.position().x()
        y = e.position().y()
        
        #Add polygon vertex
        if self.__add_vertex:
            
            #Create new point
            p = QPointF(x, y)
        
            #Add to point to polygon
            self.__pol.append(p)
        
        #Change q coordinates
        else:
            self.__q.setX(x)
            self.__q.setY(y)
        
        #Repaint screen
        self.repaint()
 
 
    def paintEvent(self, e: QPaintEvent):
        #Create new graphic object
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
      
        #Set graphic attributes, polygon
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw polygon
        qp.drawPolygon(self.__pol)
        
        #Set graphic attributes, point
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.red)
        
        #draw point
        r = 10
        qp.drawEllipse(int(self.__q.x()-r), int(self.__q.y()-r), 2*r, 2*r)
        
        #End drawing
        qp.end()
        
    def switchInput(self):
        #Input point or polygon vertex
        self.__add_vertex = not (self.__add_vertex)
    
    def getQ(self):
        #Get point
        return self.__q
    
    def getPol(self):
        #Get polygon
        return self.__pol