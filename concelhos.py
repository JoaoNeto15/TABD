import matplotlib.pyplot as plt
import numpy as np
import psycopg2

def polygon_to_points(polygon_string):
    xs, ys = [],[]
    points = polygon_string[9:-2].split(',')
    for point in points:
        (x,y) = point.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs,ys

scale=1/30000
conn = psycopg2.connect("dbname=joaoneves user=joaoneves")
cursor_psql = conn.cursor()

# Calculate figure size
sql ="select st_astext(st_envelope(st_collect(st_simplify(proj_boundary,100,FALSE)))) from cont_aad_caop2018 where concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
row = results[0]
polygon_string = row[0]
xs,ys = polygon_to_points(polygon_string)

width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1

fig = plt.figure(figsize=(width_in_inches*scale,height_in_inches*scale))

#É ESTAAAAAAA
sql = "SELECT st_astext(st_union(proj_boundary)) from cont_aad_caop2018 where distrito in ('PORTO') group by concelho"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
#print(results[0])

for row in results:
    polygon_string = row[0]
    xs, ys = polygon_to_points(polygon_string)
    plt.plot(xs,ys,color='red')

""" sql = "SELECT concelho, st_astext(st_union(proj_boundary)) from cont_aad_caop2018 where distrito in ('PORTO') group by concelho"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
print(results) """

plt.show()