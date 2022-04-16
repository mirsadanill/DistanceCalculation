import requests 
import pandas as pd
from math import radians, cos, sin, asin, sqrt, atan2, degrees,acos
import math
from datetime import datetime
import time
import dateutil.parser



rsp = requests.get("https://t58umj7xdf.execute-api.eu-central-1.amazonaws.com/test/tripdata?ident=861230043918953&timestart=2022-03-29T20:59:59&timestop=2022-03-30T20:59:59").json()


df = pd.DataFrame(rsp['Items'], columns=['SK','position_longitude', 'position_latitude','vehicle_speed','acc_x'])

def haversine(lat1, lon1, lat2, lon2):
      R = 6371
      xlat1 = (math.radians(lat1))
      xlat2 = (math.radians(lat2))
     

      dLat = (math.radians(lat2 - lat1))
      dLon = (math.radians(float(lon2) - float(lon1)))
     
      a = math.sin(dLat/2)**2 + math.cos(xlat1) * math.cos(xlat2) * math.sin(dLon/2)**2
      c = 2*asin(sqrt(a))

      return R * c
def mesafe():
    for i in range(1,len(df)):
         
       slat = radians(float(df["position_latitude"][0]))
       slon = radians(float(df["position_longitude"][0]))
       elat = radians(float(df["position_latitude"][i]))
       elon = radians(float(df["position_longitude"][i])) 
    
    dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    print("Toplam Yer değiştirme:" , dist,"km")
mesafe()
def yerdegistirme():   
    toplam=0
    for i in range(1,len(df)):
        lat1=float(df["position_latitude"][i])
        lat2=float(df["position_latitude"][i-1])
        lon1=df["position_longitude"][i]
        lon2=df["position_longitude"][i-1]
        toplam+=haversine(lat1, lon1, lat2, lon2)
        #print(haversine(lat1, lon1, lat2, lon2)*1000,"metre")
    print("Toplam mesafe:",toplam,"km")
yerdegistirme()

def hizagöremesafehesapla():
    toplam=0
    for i in range(1,len(df)):
        d = dateutil.parser.parse(df["SK"][i])
        d=d.strftime('%Y/%m/%d/%H/%M/%S')
        d=time.mktime(datetime.strptime(d, "%Y/%m/%d/%H/%M/%S").timetuple())
        t = dateutil.parser.parse(df["SK"][i-1])
        t=t.strftime('%Y/%m/%d/%H/%M/%S')
        t=time.mktime(datetime.strptime(t, "%Y/%m/%d/%H/%M/%S").timetuple())
        b=(d-t)
        speed1=df["vehicle_speed"][i]
        speed2=df["vehicle_speed"][i-1]
        a= (int(speed1)*b)/3600
        toplam+=a
    print("Toplam mesafe:",toplam,"km")
hizagöremesafehesapla()
