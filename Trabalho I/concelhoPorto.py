import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from datetime import datetime
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register


def polygon_to_points(polygon):
    xs, ys = [],[]
    for (x,y) in polygon.coords:
        xs.append(x)
        ys.append(y) 
    return xs,ys

scale=1/30000
conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
register(conn)
cursor_psql = conn.cursor()


xs_min, xs_max, ys_min, ys_max = -47000, -34000, 163000, 169000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

fig, ax = plt.subplots(figsize=(15,7.5))

#É ESTAAAAAAA
sql = "SELECT proj_boundary from cont_aad_caop2018 where concelho in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
#print(results[0])

for row in results:
    polygon = row[0][0]
    xs,ys = polygon_to_points(polygon)
    plt.plot(xs,ys,color='black',lw='0.2')

def animate(i):
    scat.set_offsets([xs[i],ys[i]])
    


scale=1/60000
conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
cursor_psql = conn.cursor()



sql = """select proj_track from tracks where taxi='20000003' order by ts"""
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

xs, ys = [], []
for track in results:
    xy = track[0].coords
    for (x,y) in xy:
        xs.append(x)
        ys.append(y)
    

scat = ax.scatter(xs[0],ys[0],s=10)
anim = FuncAnimation(
    fig, animate, interval=1, frames=len(ys)-1)

plt.draw()
plt.show()
conn.close()
