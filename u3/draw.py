from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *
from qpoint3df import *
from edge import *
from random import *
from triangle import *
from math import *

class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_points = True
        self.points = []
        self.view_dt = True
        self.dt = []
        self.view_contour_lines = True
        self.contour_lines = []
        self.view_slope = True
        self.view_aspect = True
        self.triangles = []
        
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
        
        if self.view_aspect:
            #Set graphical attributes: triangles
            qp.setPen(Qt.GlobalColor.black)
    
            #Draw slope
            for t in self.triangles:
                #Get vertices
                p1, p2, p3 = t.getVertices()
                
                #Get slope
                slope = t.getSlope()
                
                #Convert slope to color
                k = 255/pi
                color = int(255 - (k * slope)) 
            
                #Create QColor
                qcolor = QColor(color, color, color)
                qp.setBrush(qcolor)
                
                #Create polygon
                vertices = QPolygonF()
                vertices.append(p1)
                vertices.append(p2)
                vertices.append(p3)
                
                #Draw polygon
                qp.drawPolygon(vertices) 
        
        if self.view_points:
            #Set graphical attributes: points
            qp.setPen(Qt.GlobalColor.black)
            qp.setBrush(Qt.GlobalColor.yellow)
            
            #Point radius
            r = 10
            
            #Draw points 
            for p in self.points:
                #draw point
                qp.drawEllipse(int(p.x()-r), int(p.y()-r), 2*r, 2*r)
        
        if self.view_dt:
            #Set graphical attributes: delaunay triangulation
            qp.setPen(Qt.GlobalColor.gray)
            
            #Draw delaunay triangulation
            for edge in self.dt:
                qp.drawLine(edge.getStart(), edge.getEnd())
            
        if self.view_contour_lines:
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
    
    def getTriangles(self):
        # Returns list of triangles
        return self.triangles
    
    def setDT(self, dt_):
        #Set results, dt
        self.dt = dt_
        
    def setTriangles(self, triangles_):
        #Set results, triangles
        self.triangles = triangles_
        
    def setContourLines(self, contour_lines_):
        #Set contour lines 
        self.contour_lines = contour_lines_  
        
        
    def setViewPoints(self, view_points_):
        #Set view points
        self.view_points = view_points_
        
        
    def setViewDT(self,view_dt_):
        #Set view DT
        self.view_dt = view_dt_


    def setViewContourLines(self,view_contour_lines_):
        #Set view contour lines
        self.view_contour_ines = view_contour_lines_   


    def setViewSlope(self,view_slope_):
        #Set view slope
        self.view_aspect = view_slope_
    
    
    def setViewAspect(self,view_aspect_):
        #Set view aspect
        self.view_aspect = view_aspect_   
     
     
    def clearData(self):
        #Clear points and dt
        self.points.clear()
        self.dt.clear()
        
        #Repaint screen
        self.repaint()
        
        