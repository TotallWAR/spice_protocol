import datetime
import psycopg2

conn = psycopg2.connect("dbname='broker' user='broker' host='10.0.2.11' password='broker'")
cur = conn.cursor()

cur.execute("""ALTER TABLE vm_user ADD time TIMESTAMP""")

current_time = datetime.datetime.now()

cur.execute("""INSERT INTO vm_user (time) VALUES (current_time)""") 
conn.commit()