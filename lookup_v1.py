from xml.dom import minidom
import datetime

import overpy

from function import gettime, mydist, myplot, mysegmentid
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib

import re



matplotlib.use("Agg")
import matplotlib.pyplot as plt

#### smoothing length ######
seg_len = 3

starttime = datetime.datetime.now()

lat = []
lon = []
ele = []
t = []
segment = []
track_d_dis = []
track_d_time = []
track_total_time = []
track_d_ele = []
track_d_speed = []
track_d_grad = []

track_lat = []
track_lon = []
track_ele = []
track_time = []
track_node = []
track_lookup_accuracy = []

total_h = 0

print("parsing gpx file ...")
doc = minidom.parse("training_routes/strava.activities.3505434868.Afternoon-Ride.gpx")

name = doc.getElementsByTagName("name")[0]
print("Ride title", name.firstChild.data)

data = doc.getElementsByTagName("trkpt")
for trkpt in data:
    lat.append(float(trkpt.getAttribute("lat")))
    lon.append(float(trkpt.getAttribute("lon")))
    ele.append(float((trkpt.getElementsByTagName("ele")[0]).firstChild.data))
    time = trkpt.getElementsByTagName("time")[0].firstChild.data
    date_time_obj = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.000Z')
    t.append(date_time_obj)

print("done", gettime(starttime, datetime.datetime.now()), "seconds")

print("processing data ...")


class OverpassBadRequest(Exception):
    pass


api = overpy.Overpass()

num_points = len(t)
print(num_points)
seg_len = 3

#print(lat)
#for i in range(1+seg_len,num_points-seg_len,1):

sub_start = 520
sub_end = 540
i = sub_start+1
nodeid = []
for i in range(sub_start,sub_end,1):
    ###print("i = ",i)
    print((100*(i-sub_start))/(sub_end-sub_start),"% complete")
    #lat = lat[i]
   # lon = lon[i]

    ###print(lat[i],lon[i])
    #lookup node id
    rad = 0.00001


    while len(nodeid) < 1:
        rad = 0.00002+rad
        ###print("nodeid = ",nodeid,"    rad = ",rad)

        lat_a = lat[i]
        lon_a = lon[i]
        #lat_a = 51.293528
        #lon_a = -2.881425


        sdistance = 1e-10 + mydist((lat_a-rad),(lat_a + rad),(lon_a - rad),(lon_a + rad))
        ###print("search area = ",sdistance*1000,"m")

        result = api.query(f"node({lat_a - rad},{lon_a - rad},{lat_a + rad},{lon_a + rad});out;")
        nodeid = result.get_node_ids()


    lat_a = lat[i - seg_len]
    lat_b = lat[i + seg_len]
    lon_a = lon[i- seg_len]
    lon_b = lon[i + seg_len]

    distance = 1e-10 + mydist(lat_a, lat_b, lon_a, lon_b)
    total_s = gettime(t[i - seg_len], t[i + seg_len])
    total_h = total_s / 3600.0
    speed = distance / total_h
    ###print(speed,"km/h")

    d_alt = ele[i + seg_len] - ele[i - seg_len]
    current_alt = ele[i]

    track_lat.append(lat[i])
    track_lon.append(lon[i])
    track_d_dis.append(distance)
    track_d_time.append(total_h)
    track_time.append(track_d_time[-1] + total_h)
    track_d_speed.append(speed)
    track_d_ele.append(d_alt)
    track_ele.append(current_alt)
    track_d_grad.append(d_alt / distance)
    track_node.append(result.get_node_ids())
    #print(track_node)
    ###print(result.get_node_ids())
    nodeid = []
    track_lookup_accuracy.append(sdistance)
    #nodeid[i]=result.nodes.split("id=",1)[1]
    #matches = re.search(r'(?<=d)\w+', result.nodes)
    #print(matches)
    i=i+3

print("done", gettime(starttime, datetime.datetime.now()), "seconds")
print(track_node)


#import osmnx as ox
#import matplotlib.pyplot as plt

