import math
from datetime import datetime

def test_sun_position():
    
    dt_test = datetime(2019,12,11,10,9,8)
    lat = 40.6027778
    lon = -104.7416667
    dnum = 7284.214675925926
    azi = 154.43651889238595
    ele = 22.064961906859356
    refr = 0.0412382987622563
    err = 0.001
    
    d= dnum_dt(dt_test,-7)
    
    assert abs(d-dnum) < err
    
    a,e,r = sun_position_calc(dnum, lat, lon)
    
    assert abs(a-azi) < err
    assert abs(e-ele) < err
    assert abs(r-refr) < err
    
def sun_position(dt, tz, lat, lon):
    
    dnum = dnum_dt(dt,tz)
    return sun_position_calc(dnum,lat,lon)
   

def number_range(x,rmin,rmax):
    
    shift_x = x-rmin
    delta = rmax-rmin
    
#     print(shift_x,delta)
    
    return (((shift_x % delta) +delta) % delta) + rmin

def dnum_dt(dt:datetime,tz):
    
    dy1 = math.floor((dt.month + 9) /12)
    dy2 = math.floor(7* (dt.year + dy1 )/4)
    dy3 = math.floor(275 * dt.month /9)
    dy4 = 367 * dt.year - dy2 + dy3
    
    utm = dt.hour - tz +dt.minute/60 + dt.second / 3600
    
    return dy4 +dt.day  - 730531.5 + utm /24

def sun_position_calc(dnum, lat, lon, debug=False):
    
    #constants
    tau = math.pi * 2.0
    rpd = math.pi / 180.0
    
    # lat / lon in radians
    rlat = lat * rpd
    rlon = lon * rpd
    if debug: print(f'rlat: {rlat}, rlon:{rlon}')

    if debug: print(f'dnum: {dnum}')
    
    #mean lon of sun
    slon =  number_range(dnum * 0.01720279239 + 4.894967873,0, tau)
    if debug: print(f'slon: {slon}')
    
    # mean anomaly of sun
    sano = number_range(dnum * 0.01720197034 + 6.240040768 ,0, tau)
    if debug: print(f'sano: {sano}')
    
    # ecliptic lon of the sun
    ecli = slon + 0.03342305518 * math.sin(sano) + 0.0003490658504 * math.sin(2*sano)
    if debug : print(f'ecli: {ecli}')
        
    #obliquity of the ecliptic
    obli = 0.4090877234 - 0.000000006981317008 * dnum
    if debug: print(f'obli: {obli}')
    
    #right ascension of the sun
    tmpx = math.cos(obli) * math.sin(ecli)
    tmpy = math.cos(ecli)
    rasc = math.atan2(tmpx,tmpy)
    
    if debug: print(f'rasc: {rasc}')
        
    #declination
    decl = math.asin(math.sin(obli) * math.sin(ecli))
    if debug: print(f'decl: {decl}')
    
    #local sidereal time
    stim = number_range(4.894961213 + 6.300388099 * dnum + rlon ,0,tau)
    if debug: print(f'stim: {stim}')
    
    #hour angle of sun
    hang = number_range(stim - rasc,0,tau)
    if debug: print(f'hang: {hang}')
    
    # local elevation of sun
    tmpx = math.cos(decl) *math.cos(rlat) *math.cos(hang)
    elevation = math.asin(math.sin(decl) * math.sin(rlat) +tmpx )
    if debug: print(f'elevation: {elevation}')
    
    #local azimuth of the sun
    tmpx = -math.cos(decl) * math.cos(rlat) * math.sin(hang)
    tmpy =  math.sin(decl) -math.sin(rlat) *math.sin(elevation)
    azimuth = math.atan2(tmpx,tmpy)
    if debug: print(f'azimuth: {azimuth}')
    
    # azimuth & elevation in degrees
    azi_deg = number_range(azimuth / rpd ,0.0, 360.0)
    ele_deg = number_range(elevation / rpd, 0.0, 360.0)
    
    if debug: print(f'ele_deg: {ele_deg}')
    
    #refraction correction
    targ = (ele_deg +(10.3 / (ele_deg +5.11 ))) * rpd
    if debug: print(f'targ: {targ}')
        
    refraction = (1.02 / math.tan(targ)) / 60.0
    
    #adjust elevation for refraction
    ele_deg_refract = ele_deg + refraction
    
    return azi_deg, ele_deg_refract, refraction