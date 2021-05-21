import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register

conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
register(conn)
cursor_psql = conn.cursor()

def cost(id):
    #print("TaxiId: " + str(id))
    #sql = "SELECT N, ST_Distance(ST_Pointn(proj_track,N), ST_PointN(proj_track, n+1)) as D from tracks, (SELECT generate_series(1,ST_NumPoints(proj_track)-1) as N from tracks where id=" + str(id) + ") as X where id=" + str(id);
    sql = "SELECT ts,proj_track FROM tracks WHERE id="+str(id)
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    xy = results[0][1].coords
    ts = results[0][0]
    dt_object = datetime.fromtimestamp(ts)
    print(dt_object)
    if (dt_object.hour>6 and dt_object.hour<21):
        print("DIA")
        distance_fare = 212.77
        bandeirada=1800
        total_money = 3.25
    else:
        print("NOITE")
        distance_fare = 178.57
        bandeirada=1440
        total_money = 3.9
    #print(distance_fare)
    seconds = 0
    total_time=0
    total_distance=0
    distance = 0
    flag_first = 1
    flag_bandeirada = 1
    for (x,y) in xy:
        seconds+=1
        total_time+=1
        if(flag_first == 1):
            prevX = x
            prevY = y
            flag_first = 0
        else:
            distance_aux = math.sqrt(abs(x-prevX)**2+abs(y-prevY)**2)
            #print("      Dist: " + str(distance_aux))
            if(distance_aux<50):
                distance += distance_aux
                total_distance += distance_aux
                prevX=x
                prevY=y

        if(flag_bandeirada == 1):
            if distance >= bandeirada:
                flag_bandeirada = 0
                seconds = 0
                distance -= bandeirada
        else:
            if(seconds==24):
                total_money+=0.1
                seconds=0
                distance=0
                continue
            if (distance >= distance_fare):
                total_money+=0.1
                seconds=0
                distance-=distance_fare
    
    print("Custo: " + str(round(total_money,2)))
    print("Distancia: " + str(round(total_distance/1000,2)))
    print("Tempo: " + str(round(total_time/60,2)))

    return total_money

""" cost(1)
print()
cost(22)
print()
cost(54)
print()
cost(434)
print()
cost(12974)
print()
cost(12985)
print() """

def concelho():
    sql = "SELECT concelho, tracks.id from tracks, cont_aad_caop2018 WHERE state='BUSY' AND ST_Within(ST_StartPoint(proj_track), proj_boundary) order by concelho"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    print(results)



