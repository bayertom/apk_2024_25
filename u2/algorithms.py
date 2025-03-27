from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from numpy import *
from numpy.linalg import *

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
    
    
    
    def createCH(self, polygon: QPolygonF):
        """
        Create convex hull using Jarvis Scan
        """
        ch = QPolygonF()
        
        # Create pivot
        q = min(polygon, key = lambda k: k.y())
        pj = q
        
        # Create point ph1
        px = min(polygon, key = lambda k: k.x())
        pj1 = QPointF(px.x(), pj.y())
        
        # Add pivot to ch
        ch.append(pj)
        
        # Process all points
        while True:
            #Initialize maximum and its index
            phi_max = 0
            idx_max = -1
            
            for i in range(len(polygon)):
                #Different points
                if (pj != polygon[i]):
                    #Compute angle
                    phi = self.get2VectorsAngle(pj, pj1, pj, polygon[i])
            
                    #Update maximum
                    if phi > phi_max:
                        phi_max = phi
                        idx_max = i
            
            #Add point to ch
            ch.append(polygon[idx_max])
            
            #Update indices
            pj1 = pj
            pj = polygon[idx_max]
            
            #Stop
            if pj == q:
                break
        
        return ch  
    
    def rotate(self, pol: QPolygonF, sigma):
        #Rotate polygon by angle sigma
        pol_r = QPolygonF()
        
        #Process points one by one
        for p in pol:
            
            #Rotate polygon point
            x_r = p.x()*cos(sigma) - p.y()*sin(sigma)
            y_r = p.x()*sin(sigma) + p.y()*cos(sigma)
            
            #Create point
            p_r =QPointF(x_r, y_r)
            
            #Add point to polygon
            pol_r.append(p_r)
        
        return pol_r
    
    def createMMB(self, pol:QPolygonF):
        # Create min-max box
        mmb = QPolygonF()
        
        #Find extreme coordinates
        x_min = min(pol, key = lambda k: k.x()).x()
        x_max = max(pol, key = lambda k: k.x()).x()
        
        y_min = min(pol, key = lambda k: k.y()).y()
        y_max = max(pol, key = lambda k: k.y()).y()
        
        #Compute area
        area = (x_max - x_min) * (y_max - y_min)
        
        #Create min-max box vertices
        v1 = QPointF(x_min, y_min)
        v2 = QPointF(x_max, y_min)
        v3 = QPointF(x_max, y_max)
        v4 = QPointF(x_min, y_max)
        
        #Create min-max box polygon
        mmb.append(v1)
        mmb.append(v2)
        mmb.append(v3)
        mmb.append(v4)
        
        return mmb, area
    
    
    def getArea(self, pol: QPolygonF):
        # Compute area of a polygon
        area = 0
        n = len(pol)
        
        #Process vertices one by one
        for i in range(n):
            area += pol[i].x()*(pol[(i+1)%n].y()-pol[(i-1+n)%n].y())
            
        return abs(area)/2
    
        
    def resizeRectangle(self,building:QPolygonF, mbr:QPolygonF):
        # Resizing rectangle to match the building area
        mbr_res = QPolygonF()
                    
        #Compute k
        Ab = self.getArea(building)
        A = self.getArea(mbr)
        k = Ab / A
        
        # Compute centroid
        x_t = 0.25*(mbr[0].x()+mbr[1].x()+mbr[2].x()+mbr[3].x())
        y_t = 0.25*(mbr[0].y()+mbr[1].y()+mbr[2].y()+mbr[3].y())
        
        #Compute vectors
        v1_x = mbr[0].x() - x_t
        v1_y = mbr[0].y() - y_t
        
        v2_x = mbr[1].x() - x_t
        v2_y = mbr[1].y() - y_t
        
        v3_x = mbr[2].x() - x_t
        v3_y = mbr[2].y() - y_t
        
        v4_x = mbr[3].x() - x_t
        v4_y = mbr[3].y() - y_t
        
        #Compute coordinates of resized points
        v1_xr = x_t + v1_x * sqrt(k)
        v1_yr = y_t + v1_y * sqrt(k)
        
        v2_xr = x_t + v2_x * sqrt(k)
        v2_yr = y_t + v2_y * sqrt(k)
        
        v3_xr = x_t + v3_x * sqrt(k)
        v3_yr = y_t + v3_y * sqrt(k)
        
        v4_xr = x_t + v4_x * sqrt(k)
        v4_yr = y_t + v4_y * sqrt(k)
        
        #Create new vertices
        v1_res = QPointF(v1_xr, v1_yr)
        v2_res = QPointF(v2_xr, v2_yr)
        v3_res = QPointF(v3_xr, v3_yr)
        v4_res = QPointF(v4_xr, v4_yr)
        
        #Add vertices to the resized mbr
        mbr_res.append(v1_res)
        mbr_res.append(v2_res)
        mbr_res.append(v3_res)
        mbr_res.append(v4_res)
        
        return mbr_res
    

    def createMBR(self, building: QPolygonF):
        #Simplify building using MBR
        sigma_min = 0
        
        #Create convex hull
        ch = self.createCH(building)
        
        #Initilize MBR a its area
        mmb_min, area_min = self.createMMB(ch)

        #Browse CH segments
        n = len(ch)
        
        for i in range(n): 
            
            #Coordinate differences
            dx = ch[(i+1)%n].x() - ch[i].x()
            dy = ch[(i+1)%n].y() - ch[i].y()
            
            #Compute direction
            sigma = atan2(dy, dx)
            
            #Rotate polygon
            ch_r = self.rotate(ch, -sigma)
            
            #Compute min-max box 
            mmb, area = self.createMMB(ch_r)
            
            #Update minimum
            if area < area_min:
                area_min = area 
                mmb_min = mmb
                sigma_min = sigma
                
        #Resize rectangle
        mmb_min_res = self.resizeRectangle(building,mmb_min)
        
        #Convert min-max box with the minimum area to MBR
        return self.rotate(mmb_min_res, sigma_min)
    
    
    def createBRPCA(self, building: QPolygonF):
        #Simplify building using PCA
        x, y = [], []
        
        #Convert points to coordinates
        for p in building:
            x.append(p.x())
            y.append(p.y())
            
        #Create A
        A = array([x, y])
            
        #Covariance matrix
        C = cov(A)
        
        #Singular value decomposition
        [U, S, V] = svd(C)
        
        #Direction of the principal vector
        sigma = atan2(V[0][1],V[0][0])
        
        #Rotate polygon
        building_r = self.rotate(building, -sigma)
        
        #Compute min-max box 
        mmb, area = self.createMMB(building_r)
        
        #Resize rectangle
        mmb_res = self.resizeRectangle(building,mmb)
        
        #Convert min-max box with the minimum area to MBR
        return self.rotate(mmb_res, sigma)
    