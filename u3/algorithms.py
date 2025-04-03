from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

from qpoint3df import *
from edge import *

class Algorithms:
    def __init__(self):
        pass
    
    def get2VectorsAngle(self, p1: QPointF, p2: QPointF, p3: QPointF, p4:QPointF):
        # Compute angle between two vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()
        
        # Dot product
        uv = ux*vx + uy*vy
        
        # Norms u, v
        norm_u = sqrt(ux**2 + uy**2)
        norm_v = sqrt(vx**2 + vy**2)
        
        #Compute argument
        arg = uv/(norm_u*norm_v)
        
        #Correct argument to interval <-1, 1>
        arg = min(max(arg, -1), 1)
        
        return acos(arg)
    
    def analyzePointAndLinePosition(self, p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF):
        #Analyzes point and line position
        eps = 1.0e-6
        
        #Vectors        
        ux, uy = p2.x() - p1.x(), p2.y() - p1.y()
        vx, vy = p.x() - p1.x(), p.y() - p1.y()
        
        #Determinant test
        t = ux*vy-uy*vx
        
        #Returns left: 1; right: -1; on line: 0
        if t > eps:
            return 1
        
        if t < -eps:
            return -1
        
        return 0
    
        
    def distance2D(self, p1: QPoint3DF, p2:QPoint3DF):
        #compute 2D distance between two points
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        
        return sqrt(dx**2 + dy**2)
    
    
    def getNearestPoint(self, q:QPoint3DF, points: list[QPoint3DF]):
        #Get point nearest to query point
        min_dist = 1.0e-16
        nearest_point = None
        
        #Process points one by one
        for point in points:
            #Compute distance
            dist = self.distance2D(q, point)
            
            #Update minimum
            if q != points[i] and dist < min_dist :
                min_dist = dist
                nearest_point = point
                
        return nearest_point
    
    def findDelaunayPoint(self, p1:QPoint3DF, p2:QPoint3DF, points: list[QPoint3DF]):
        #Find Optimal Delaunay Point
        omega_max = 0
        delaunay_point = None
        
        #process points one by one
        for point in points:
            
            #Point in the left half plane
            if self.analyzePointAndLinePosition(point, p1, p2) == 1:
            
                #Compute omega
                omega = self.get2VectorsAngle(point, p1, point, p2)
                
                #Update maximum
                if omega > omega_max:
                    omega_max = omega
                    delaunay_point = point
    
        return delaunay_point
        
    def delaunayTriangulation(self, points: list[QPoint3DF]):
        #Construct Delaunay Triangulation, incremental method
        dt = [] #list[Edges]
        ael = [] #listof active edges
        
        #finding a point with minimum x
        p1 = min(points, key=lambda k:k.x())
        
        # find nearest point
        p2 = self.getNearestPoint(p1,points)
        
        # create new edges
        e = Edge(p1,p2)
        es = Edge(p2,p1)
        
        