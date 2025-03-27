from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *


class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.building = QPolygonF()
        self.building_simp = QPolygonF()
        
        
    def mousePressEvent(self, e: QMouseEvent):
        
        #Get coordinates of q
        x = e.position().x()
        y = e.position().y()
                
        #Create temporary point
        p = QPointF(x, y)
        
        #Add p to polygon
        self.building.append(p)
            
        #Repaint screen
        self.repaint()
        
        
    def paintEvent(self, e: QPaintEvent):
        #Draw situation
        
        #Create new graphic object
        qp = QPainter(self)
        
        #Start drawing
        qp.begin(self)
        
        #Set graphical attributes: building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw building
        qp.drawPolygon(self.building)
        
        #Set graphical attributes: building_simplify
        qp.setPen(Qt.GlobalColor.gray)
        qp.setBrush(Qt.GlobalColor.blue)
        
        #Draw building simplify
        qp.drawPolygon(self.building_simp)
        
        #End drawing
        qp.end()
        
    
    def getBuilding(self):
        # Return analyzed building
        return self.building
    
    
    def setSimplifBuilding(self, building_simp_):
        self.building_simp = building_simp_
    
    
    def clearData(self):
        #Clear polygon
        self.building.clear()
        
        #Repaint screen
        self.repaint()
        