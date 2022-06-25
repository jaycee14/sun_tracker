from pysolar.solar import *
from datetime import datetime, timedelta
import pytz

#vounaki greece
latitude =38.771111
longitude=20.880278

date = datetime(2021, 9, 23, 0, 0, 0,0)
#date =datetime.datetime.now()
tz = pytz.timezone("Europe/Athens")
date=tz.localize(date)
print(date)
print(get_altitude(latitude, longitude, date))

dt=10 #mins
num_dt = int(24 * 60 / dt)


def surface_point(height, alt_angle):
	
	return height / math.tan(alt_angle * math.pi / 180)


for i in range(num_dt):
	nt = date + timedelta(minutes=i*10)
	alt_angle = get_altitude(latitude, longitude, nt)
	az_angle = get_azimuth(latitude,longitude,nt)
	print(nt, alt_angle, az_angle )
	
	print(surface_point(2,alt_angle))