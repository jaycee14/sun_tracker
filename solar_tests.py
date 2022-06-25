from pysolar.solar import *
import datetime
import pytz

#latitude = 42.206
#longitude = -71.382

latitude =38.771111
longitude=20.880278

#date = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=datetime.timezone.utc)
date =datetime.datetime.now()
tz = pytz.timezone("Europe/Athens")
date=tz.localize(date)
print(date)
print(get_altitude(latitude, longitude, date))