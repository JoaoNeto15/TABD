import matplotlib.pyplot as plt
import matplotlib.animation as animation
import psycopg2
import math
from postgis import Polygon, MultiPolygon, LineString
from postgis.psycopg import register


conn = psycopg2.connect("dbname=taxi_services user=joao")
register(conn)
cursor_psql = conn.cursor()


sql = "SELECT ST_Simplify( ST_Union() )"

