from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Algorithms:
    def __init__(self):
        pass
    
    def ray_crossing(q:QPointF,pol:QPolygonF):
        # analyze point and polygon position using ray crossing algorithm
        k = 0 #amount of intersection points
        n = len(pol)
        for i in range(n): #process all points
            
            #Get i-th point
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            
            #Get (i+1)st point
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()
            
            #Test criterion
            if (yi1r > 0) and (yir <= 0) or (yi1r <= 0) and (yir > 0):
                # We found a suitable segment, now we compute intersection
                xm = (xi1r*yir - xir*yi1r)/(yi1r-yir)
                
                if xm > 0:
                    # if m is in the right half-plane; increase number of k 
                    k = k + 1
        return k%2