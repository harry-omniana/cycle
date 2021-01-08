import numpy as np
from math import sin, cos, sqrt, atan2, radians
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import overpy


####### Time to s function ######
def gettime(t_a, t_b):
    t_diff = relativedelta(t_b, t_a)  # later/end time comes first!
    '{h}h {m}m {s}s'.format(h=t_diff.hours, m=t_diff.minutes, s=t_diff.seconds)
    total_s = (3600.0 * t_diff.hours) + (60.0 * t_diff.minutes) + t_diff.seconds
    return (total_s)


######## distance function ########
def mydist(lat1, lat2, lon1, lon2):
    rlat1 = radians(lat1)
    rlat2 = radians(lat2)
    rlon1 = radians(lon1)
    rlon2 = radians(lon2)

    R = 6373.0

    dlon = rlon2 - rlon1
    dlat = rlat2 - rlat1
    a = (sin(dlat / 2)) ** 2 + cos(rlat1) * cos(rlat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return (distance)


#### plot function
def myplot(x, y, colour):
    color1 = [str(item / max(colour)) for item in colour]
    fig = plt.figure()
    plt.scatter(x, y, s=5, c=color1)

    return (fig)


#### open street map ID lookup
def mysegmentid(lat_a, lon_a, rad):
    api = overpy.Overpass()
    result = api.query(f"node({lat_a - rad},{lon_a - rad},{lat_a + rad},{lon_a + rad});out;")
    nodeid = result.get_node_ids()
    return (nodeid)
