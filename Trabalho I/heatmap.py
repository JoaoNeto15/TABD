import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns;
import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register


minx = -46843.16270000022
miny = 163345.06010000035

a = np.zeros((53, 116))

conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
register(conn)
cursor_psql = conn.cursor()

sql ="select final_point_proj from taxi_services, cont_aad_caop2018 where st_within(final_point_proj,proj_boundary) and concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

for result in results:
    (x,y) = result[0].coords
    y1=int((y-miny)/100)
    x1=int((x-minx)/100)
    a[y1][x1] = a[y1][x1] + 1

""" print(len(xs))
print(len(ys))
print(min(xs),max(xs))
print(max(xs)-min(xs))
print(min(ys),max(ys))
print(max(ys)-min(ys)) """
    

    





fig = plt.figure(figsize=(12,5.2))



ax = sns.heatmap(a, vmax=10000)
ax.invert_yaxis()

"""
select id, st_astext(initial_point), st_astext(initial_point_proj) from taxi_services order by ST_Y(initial_point) limit 10;
select count(*) from taxi_services, cont_aad_caop2018 where st_within(initial_point_proj,proj_boundary);

select id, st_astext(initial_point) from taxi_services, cont_aad_caop2018 where st_within(initial_point_proj,proj_boundary)order by ST_Y(initial_point) limit 10;
"""



#É ESTAAAAAAA
sql = "SELECT proj_boundary from cont_aad_caop2018 where concelho in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

for row in results:
    xs=[]
    ys=[]
    for (x,y) in row[0][0].coords:
        if(x<minx):
            minx=x
        if(y<miny):
            miny=y
        xs.append((x-minx)/100)
        ys.append((y-miny)/100)
    plt.plot(xs,ys,color='white',lw='0.5')


""" print("x:")
print(minx, maxx)
print("y:")
print(miny, maxy) """



plt.show()
conn.close()
