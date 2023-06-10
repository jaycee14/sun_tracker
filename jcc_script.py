import math
import time


def rnge(x, rmin, rmax):
    shiftedx = x - rmin
    delta = rmax - rmin
    return (((shiftedx % delta) + delta) % delta) + rmin


def sunpos(ticks, time_zone, latitude, longitude):
    # Trig constants
    tau = math.pi * 2.0
    rpd = math.pi / 180.0

    # Latitude/longitude in radians
    rlat = latitude * rpd
    rlon = longitude * rpd

    # Calculate dnum from ticks in this version
    dnum = ticks / 86400.0 - 10957.791666666667 - time_zone / 24.0

    print(dnum, ticks)  ##################  added for debugging

    # Mean longitude of the sun
    slon = rnge(dnum * 0.01720279239 + 4.894967873, 0, tau)

    # Mean anomaly of the Sun
    sano = rnge(dnum * 0.01720197034 + 6.240040768, 0, tau)

    # Ecliptic longitude of the sun
    ecli = slon + 0.03342305518 * math.sin(sano) + 0.0003490658504 * math.sin(2 * sano)

    # Obliquity of the ecliptic
    obli = 0.4090877234 - 0.000000006981317008 * dnum

    # Right ascension of the sun
    tmpx = math.cos(obli) * math.sin(ecli)
    tmpy = math.cos(ecli)
    rasc = math.atan2(tmpx, tmpy)

    # Declination of the sun
    decl = math.asin(math.sin(obli) * math.sin(ecli))

    # Local sidereal time
    stim = rnge(4.894961213 + 6.300388099 * dnum + rlon, 0, tau)

    # Hour angle of the sun
    hang = rnge(stim - rasc, 0, tau)

    # Local elevation of the sun
    tmpx = math.cos(decl) * math.cos(rlat) * math.cos(hang)
    elevation = math.asin(math.sin(decl) * math.sin(rlat) + tmpx)

    # Local azimuth of the sun
    tmpx = -math.cos(decl) * math.cos(rlat) * math.sin(hang)
    tmpy = math.sin(decl) - math.sin(rlat) * math.sin(elevation)
    azimuth = math.atan2(tmpx, tmpy)

    # Convert azimuth and elevation to degrees
    azimuth = rnge(azimuth / rpd, 0.0, 360.0)
    elevation = rnge(elevation / rpd, -180.0, 180.0)

    # Refraction correction
    targ = (elevation + (10.3 / (elevation + 5.11))) * rpd
    refraction = (1.02 / math.tan(targ)) / 60.0

    # Adjust elevation for refraction
    elevation = elevation + refraction

    # Return azimuth, elevation, and refraction
    return (azimuth, elevation, refraction)


def main():
    ticks = time.mktime((2019, 12, 11, 10, 9, 8, 0, 0, 0))
    time_zone = -7
    latitude = 40.6027778
    longitude = -104.7416667

    azimuth, elevation, refraction = sunpos(ticks, time_zone, latitude, longitude)

    print(time.asctime(time.localtime(ticks)))
    print("time_zone:", time_zone)
    print("latitude:", latitude)
    print("longitude:", longitude)
    print("")
    print("Azimuth:", azimuth)
    print("Elevation:", elevation)
    print("Refraction:", refraction)
    print()


if __name__ == "__main__":
    main()