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


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def cost(id):
    #print("TaxiId: " + str(id))
    # Select ST_length(proj_track) from tracks where id=1;
    #sql = "SELECT N, ST_Distance(ST_Pointn(proj_track,N), ST_PointN(proj_track, n+1)) as D from tracks, (SELECT generate_series(1,ST_NumPoints(proj_track)-1) as N from tracks where id=" + str(id) + ") as X where id=" + str(id);
    sql = "SELECT ts,proj_track, ST_length(proj_track) FROM tracks WHERE id="+str(id)
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    xy = results[0][1].coords
    ts = results[0][0]
    dt_object = datetime.fromtimestamp(ts)
    #print(dt_object)
    if (dt_object.hour>6 and dt_object.hour<21):
        #print("DIA")
        distance_fare = 212.77
        bandeirada=1800
        total_money = 3.25
    else:
        #print("NOITE")
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
    #print(len(xy))
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
            if(distance_aux<56):
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
    
    """ print("Custo: " + str(round(total_money,2)) + "€")
    print("Distancia Query: " + str(round(results[0][2]/1000,2)))
    print("Distancia: " + str(round(total_distance/1000,2)) + "km")
    print("Tempo: " + convert(total_time)) """

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
    concelhos = ["PORTO", "VILA NOVA DE GAIA", "MATOSINHOS", "GONDOMAR", "MAIA"]
    cost_concelhos = [[0,0],[0,0],[0,0],[0,0],[0,0]]
    for i in range(len(concelhos)):
        sql = "SELECT tracks.id from tracks, cont_aad_caop2018 WHERE state='BUSY' AND concelho='"+ concelhos[i] +"' AND ST_Within(ST_StartPoint(proj_track), proj_boundary)"
        cursor_psql.execute(sql)
        results = cursor_psql.fetchall()
        print(concelhos[i] + ": " + str(len(results)))
        cost_concelhos[i][1] = len(results)
        for j in results:
            cost_concelhos[i][0] += cost(j[0])
    print(cost_concelhos)
    for i in cost_concelhos:
        print("%.2f/%d=%.2f" % (i[0],i[1], i[0]/i[1]))
        



concelho()