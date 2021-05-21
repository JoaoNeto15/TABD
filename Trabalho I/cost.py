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
    sql = "SELECT ts,proj_track FROM tracks WHERE id="+str(id)
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    xy = results[0][1].coords
    ts = results[0][0]
    dt_object = datetime.fromtimestamp(ts)
    print(dt_object)
    if (dt_object.hour>9 and dt_object.hour<21):
        #print("DIA")
        distance_fare = 212.77
    else:
        #print("NOITE")
        distance_fare = 178.57
    seconds = 0
    total_time=0
    total_distance=0
    total_money = 0.0
    distance = 0
    first = 1
    for (x,y) in xy:
        seconds+=1
        total_time+=1
        if(first == 1):
            prevX = x
            prevY = y
            first = 0
        else:
            distance_aux = math.sqrt(abs(x-prevX)**2+abs(y-prevY)**2)
            if(distance_aux<50):
                distance += distance_aux
                total_distance += distance_aux
                prevX=x
                prevY=y

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


