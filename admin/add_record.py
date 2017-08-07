# coding=utf-8
import psycopg2


new_db_name = "broker"
new_user = "broker"
_host = "localhost"




# Input user name and check exising of user
userId = raw_input("Please user id: ")

try:
    con = psycopg2.connect(dbname="broker", user="broker", password="broker", host=_host)
except Exception as e:
    print e.message
    # print "I am unable to connect to the database"
    con = None

# Set autocommit to correct creating DB
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

# Check existing of user
cur.execute("SELECT id FROM foreign_nova;")

user = cur.fetchall()

print "\nShow me the databases:\n"
for row in user:
    print "   ", row[0]

cur.close()
con.close()