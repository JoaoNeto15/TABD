import matplotlib.pyplot as plt
import numpy as np
import psycopg2
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register
import math

conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
register(conn)
cursor_psql = conn.cursor()

def cost(id):
    sql = "SELECT proj_track FROM tracks WHERE id="+str(id)
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    xy = results[0][0].coords
    seconds = 0
    money = 0.0
    distance = 0
    first = 1
    for (x,y) in xy:
        seconds+=1
        if(seconds==24):
            money+=0.1
            seconds=0
            distance=0
            continue
        if(first == 1):
            prevX = x
            prevY = y
            first = 0
        else:
            distance_aux = math.sqrt(abs(x-prevX)**2+abs(y-prevY)**2)
            if(distance_aux<50):
                distance += distance_aux
                prevX=x
                prevY=y
            print(str(distance)+" | "+str(distance_aux)+" | " + str(seconds)+ " | " + str(money))
        if (distance > 212.77):
            money+=0.1
            seconds=0
            distance=0
    


cost(1)