import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
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

# Calculate figure size
sql ="select st_envelope(st_collect(st_simplify(proj_boundary,100,FALSE))) from cont_aad_caop2018 where concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

polygon= results[0][0][0]

xs,ys = polygon_to_points(polygon)

width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1

fig = plt.figure(figsize=(width_in_inches*scale,height_in_inches*scale))

#É ESTAAAAAAA
sql = "SELECT concelho,st_union(proj_boundary) from cont_aad_caop2018 where distrito in ('PORTO') group by concelho"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
#print(results[0])
col=0

for row in results:
    polygon = row[1][0]
    xs,ys = polygon_to_points(polygon)
    plt.plot(xs,ys,color='black',lw='0.2')
    plt.fill(xs,ys,"b", alpha=col)
    col=col+0.055

plt.show()