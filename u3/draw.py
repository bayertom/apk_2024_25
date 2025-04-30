from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *
from qpoint3df import *
from edge import *
from random import *

class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.points = []
        self.dt = []
        self.contour_lines = []
        
        #Points
        #p1 = QPoint3DF(0,0,0)
        #p2 = QPoint3DF(100,0,0)
        #p3 = QPoint3DF(100,100,0)
        
        #self.points.append(p1)
        #self.points.append(p2)
        #self.points.append(p3)
        
        
    def mousePressEvent(self, e: QMouseEvent):
        
        #Get coordinates of q
        x = e.position().x()
        y = e.position().y()
                
        #Random height
        zmin = 150
        zmax = 1500
        z = random()*(zmax-zmin)+zmin

        
        #Create temporary point
        p = QPoint3DF(x, y, z)
        
        #Add p to polygon
        self.points.append(p)
            
        #Repaint screen
        self.repaint()
        
        
    def paintEvent(self, e: QPaintEvent):
        #Draw situation
        
        #Create new graphic object
        qp = QPainter(self)
        
        #Start drawing
        qp.begin(self)
        
        #Set graphical attributes: points
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Point radius
        r = 10
        
        #Draw points 
        for p in self.points:
            #draw point
            qp.drawEllipse(int(p.x()-r), int(p.y()-r), 2*r, 2*r)
        
        #Set graphical attributes: delaunay triangulation
        qp.setPen(Qt.GlobalColor.gray)
        
        #Draw delaunay triangulation
        for edge in self.dt:
            qp.drawLine(edge.getStart(), edge.getEnd())
            
        
        #Set graphical attributes: contour lines
        qp.setPen(Qt.GlobalColor.green)
        
        #Draw contour lines
        for edge in self.contour_lines:
            qp.drawLine(edge.getStart(), edge.getEnd())
            
        #End drawing
        qp.end()
        
    
    def getPoints(self):
        # Returns input points
        return self.points
    
    
    def getDT(self):
        # Returns Delaunay triangulation
        return self.dt
    
    
    def setDT(self, dt_):
        #Set results, dt
        self.dt = dt_
        

    def setContourLines(self, contour_lines_):
        #Set contour lines 
        self.contour_lines = contour_lines_  
        
    
    def clearData(self):
        #Clear points and dt
        self.points.clear()
        self.dt.clear()
        
        #Repaint screen
        self.repaint()
        
        