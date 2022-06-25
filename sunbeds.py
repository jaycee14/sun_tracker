import math

PIXS_TO_METRE = 100

class Point:
	
	def __init__(self,x,y,h):
		self.x=x
		self.y=y
		self.h=h
		self.x_m=self.scale_pix_to_metres(x)
		self.y_m=self.scale_pix_to_metres(y)
		
	def scale_pix_to_metres(self,val):
		return int(val / PIXS_TO_METRE)
	
	def scale_metres_to_pix(self,val):
		return int(val * PIXS_TO_METRE)
	
	def project(self, alt_angle, az_angle):
# 		az_angle = az_angle +180
# 		alt_angle=45
		rad = self.h / math.tan(alt_angle * math.pi/180)
		delta_x = rad * math.sin(az_angle * math.pi/180)
		delta_y = rad * math.cos(az_angle * math.pi/180)
		
# 		print(f'delta x: {delta_x} delta_y: {delta_y}')
		
# 		return self.scale_metres_to_pix(self.x_m + delta_x), self.scale_metres_to_pix(self.y_m + delta_y)
		return self.x + delta_x, self.y+delta_y 
		
	def get_point(self):
		return self.x,self.y
    
class Circle:
    
    def __init__(self,x,y,radius,n_points, height):
        
        self.pts=[]
        angle_rad = (2 * math.pi) / n_points
        for p in range(n_points):
            x_pos = radius * math.sin(angle_rad * p)
            y_pos = radius * math.cos(angle_rad * p)
            self.pts.append(Point(x+x_pos,y+y_pos,height))
            
    def get_points(self):
        res=[]
        for pt in self.pts:
            res.append(pt.get_point())
        
        return res
    
    def project(self,alt_angle, az_angle):
        
        projected_pts=[]
        for pt in self.pts:
#             new_pt = pt.project(alt_angle, az_angle)
            projected_pts.append(pt.project(alt_angle, az_angle))
            
        return projected_pts
    

class Square:
	#x1 # top left
	#x2 # top right
	#y1 # bottom left
	#y2 # bottom right
	
#e.g. [(x1, y1), (x2, y2), (x3, y3)]
	
	def __init__(self, x,y,w,h,height):
		self.x1=Point(x,y,height)
		self.x2=Point(x+w,y,height)
		self.y1 = Point(x,y+h,height)
		self.y2 = Point(x+w,y+h,height)
		
	def get_location(self):
		return (self.x1.get_point(), self.x2.get_point(), self.y2.get_point(), self.y1.get_point()) 

	def project(self,alt_angle,az_angle):
		
		return (self.x1.project(alt_angle,az_angle), self.x2.project(alt_angle,az_angle), self.y2.project(alt_angle,az_angle), self.y1.project(alt_angle,az_angle))