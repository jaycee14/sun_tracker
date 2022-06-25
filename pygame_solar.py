import pygame
import math
from pysolar.solar import *
from datetime import datetime, timedelta
import pytz

#vounaki greece
latitude =38.771111
longitude=20.880278

PIXS_TO_METRE = 100

print('start')

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
		az_angle = az_angle +180
		rad = self.h / math.tan(alt_angle * math.pi / 180)			
		delta_x = rad * math.cos(az_angle * math.pi/180)
		delta_y = rad * math.sin(az_angle * math.pi/180)
		
		#print(f'delta x: {delta_x} delta_y: {delta_y}')
		
		return self.scale_metres_to_pix(self.x_m + delta_x), self.scale_metres_to_pix(self.y_m - delta_y)
		
	def get_point(self):
		return self.x,self.y

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

def main():

	date = datetime(2021, 9, 26, 17, 6, 0,0)
	tz = pytz.timezone("Europe/Athens")
	date=tz.localize(date)
	print(date)
	alt=get_altitude(latitude, longitude, date)
	az=get_azimuth(latitude,longitude,date)
	
	red_colour = (255,0,0)
	green_colour=(0,255,0)
	
	square = Square(100, 100, 100,100, 2)
	
	cabana = square.get_location()	
	print(cabana)
	shadow = square.project(alt,az)
	print(shadow)
		
	pygame.init()
	surface = pygame.display.set_mode((600,500))	
	pygame.draw.polygon(surface, red_colour, cabana)		
	pygame.draw.polygon(surface,green_colour,shadow)

	pygame.display.flip()

												
	while True:
		for event in pygame.event.get():
			# determin if X was clicked, or Ctrl+W or Alt+F4 was used
			if event.type == pygame.QUIT:
				return
				
print('run main')
main()
