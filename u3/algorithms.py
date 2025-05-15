from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

from qpoint3df import *
from edge import *
from triangle import *

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
        t = ux*vy - uy*vx
        
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
        min_dist = 1.0e16
        nearest_point = None
        
        #Process points one by one
        for point in points:
            
            #Compute distance
            dist = self.distance2D(q, point)
            
            #Update minimum
            if q != point and dist < min_dist :
                min_dist = dist
                nearest_point = point
                
        return nearest_point
    
    
    def findDelaunayPoint(self, p1:QPoint3DF, p2:QPoint3DF, points: list[QPoint3DF]):
        #Find Optimal Delaunay Point
        omega_max = 0
        delaunay_point = None
        
        #process points one by one
        for point in points:
           
            #Different points
            if point != p1 and point != p2:
                
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
        dt = []
        ael = []
        
        #Find a point with minimum x
        p1 = min(points, key=lambda k:k.x())
        
        #Find nearest point
        p2 = self.getNearestPoint(p1,points)
        
        #Create new edges
        e = Edge(p1,p2)
        es = Edge(p2,p1)
        
        #Add edges to ael
        ael.append(e)
        ael.append(es)
        
        #Repeat until ael is empty
        while ael:
            #Take first edge
            e1 = ael.pop()
            
            #Switch orientation
            e1s = e1.switchOrientation()
            
            #Find delaunay point
            p = self.findDelaunayPoint(e1s.getStart(), e1s.getEnd(), points)
            
            if p:
                #Create new edges
                e2s = Edge(e1s.getEnd(), p)
                e3s = Edge(p, e1s.getStart())
                
                #Add edges to dt
                dt.append(e1s)
                dt.append(e2s)
                dt.append(e3s)
                
                #Update ael
                self.update_ael(e2s, ael)
                self.update_ael(e3s, ael)
                
        return dt
        
    
    def update_ael(self, e, ael):
        """search for edge with opposite orientation"""
        
        #Switch orientation
        es = e.switchOrientation()
        
        #Edge with opposite orientation in AEL, remove
        if es in ael:
            ael.remove(es)
            
        #Edge with opposite orientation not found in AEL, add new edge
        else:
            ael.append(e)


    def contourPoint(self, p1:QPoint3DF, p2:QPoint3DF, z:float):
        # Intersection of triangle edge and horizontal plane
        xb = (p2.x()-p1.x())/(p2.getZ()-p1.getZ())*(z-p1.getZ())+p1.x()
        yb = (p2.y()-p1.y())/(p2.getZ()-p1.getZ())*(z-p1.getZ())+p1.y()
        
        return QPoint3DF(xb,yb,z)


    def createContourLines(self, dt: list[Edge], zmin: float, zmax: float, dz: float):
        #create contour lines inside the interval zmin-zmax with a given step dz
        contour_lines = []
        
        #Create contour line one by one
        for z in range(zmin, zmax, dz):
            
            #Browse all triangles
            for i in range(0, len(dt), 3):
                #Vertices of triangle
                p1 = dt[i].getStart()
                p2 = dt[i+1].getStart()
                p3 = dt[i+2].getStart()
                
                #Heights diferences
                dz1 = z - p1.getZ()
                dz2 = z - p2.getZ()
                dz3 = z - p3.getZ()
                
                #Triangle coplanar
                if dz1 == 0 and dz2 == 0 and dz3 == 0:
                    continue
                
                #Edge p1, p2 is colinear
                elif dz1 == 0 and dz2 == 0:
                    contour_lines.append(dt[i])
                    
                #Edge p2, p3 is colinear
                elif dz2 == 0 and dz3 == 0:
                    contour_lines.append(dt[i+1])
                    
                #Edge p3, p1 is colinear
                elif dz3 == 0 and dz1 == 0:
                    contour_lines.append(dt[i+2])
                    
                #Edges p1, p2 and p2, p3 intersected by plane
                elif dz1 * dz2 <= 0 and dz2 * dz3 <= 0:
                    #Compute edge-plane intersections
                    a = self.contourPoint(p1, p2, z)
                    b = self.contourPoint(p2, p3, z)
                    
                    #Create edge 
                    e = Edge(a, b)
                    
                    #Add edge to contour lines
                    contour_lines.append(e)
                    
                #Edges p2, p3 and p3, p1 intersected by plane
                elif dz2 * dz3 <= 0 and dz3 * dz1 <= 0:
                    #Compute edge-plane intersections
                    a = self.contourPoint(p2, p3, z)
                    b = self.contourPoint(p3, p1, z)
                    
                    #Create edge 
                    e = Edge(a, b)
                    
                    #Add edge to contour lines
                    contour_lines.append(e)
                    
                #Edges p3, p1 and p1, p2 intersected by plane
                elif dz3 * dz1 <= 0 and dz1 * dz2 <= 0:
                    #Compute edge-plane intersections
                    a = self.contourPoint(p3, p1, z)
                    b = self.contourPoint(p1, p2, z)
                    
                    #Create edge 
                    e = Edge(a, b)
                    
                    #Add edge to contour lines
                    contour_lines.append(e)
                    
        return contour_lines
    
    
    def computeSlope(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF):
        #Compute triangle slope
        ux, uy, uz = p3.x() - p2.x(), p3.y() - p2.y(), p3.getZ() - p2.getZ()
        vx, vy, vz = p1.x() - p2.x(), p1.y() - p2.y(), p1.getZ() - p2.getZ()
        
        #Normal vector - Vector (cross) product
        nx = uy*vz - uz*vy
        ny = -(ux*vz - uz*vx)
        nz = ux*vy - uy*vx
        
        #Norm
        n = sqrt(nx**2 + ny**2 + nz**2)
        
        return acos(nz/n)
        
    
    def convertDTToTriangles(self, dt: list[Edge], triangles: list[Triangle]):
        #Converts list of edges to list of triangles
         
        #Browse all triangles
        for i in range(0, len(dt), 3):
            #Vertices of triangle
            p1 = dt[i].getStart()
            p2 = dt[i+1].getStart()
            p3 = dt[i+2].getStart()
        
            #Create triangle
            triangle = Triangle(p1, p2, p3, 0, 0)
            
            #Add triangle to the list
            triangles.append(triangle)
            
    
    def analyzeDTMSlope(self, dt, triangles):
        #Compute slope of all triangles
        if len(triangles) == 0:
            self.convertDTToTriangles(dt, triangles)
            
        #Browse all triangles
        for t in triangles:
            #Get vertices
            p1, p2, p3 = t.getVertices()
            
            #Compute slope
            slope = self.computeSlope(p1, p2, p3)
            
            #Set slope
            t.setSlope(slope)
    