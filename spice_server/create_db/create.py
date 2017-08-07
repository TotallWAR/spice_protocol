#! /usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

new_db_name = "broker"
new_user = "broker"
_host = "10.0.2.11"




# Create new user and DB

try:
    con = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host=_host)
except Exception as e:
    print e.message
    # print "I am unable to connect to the database"
    con = None


# Set autocommit to correct creating DB
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

# Create new DB
cur.execute("CREATE DATABASE " + new_db_name + ";")
cur.execute("CREATE USER " + new_user +  " WITH password %s;", (new_user,))
cur.execute("GRANT ALL PRIVILEGES ON DATABASE " + new_db_name + " TO " + new_user + ";")

cur.close()
con.close()




# Try to connect to new DB and create Extension under user postgres
try:
    con = psycopg2.connect(dbname=new_db_name, user="postgres", password="postgres", host=_host)
except Exception as e:
    print e.message
    con = None

# Create cursor
print con

cur = con.cursor()


cur.execute("ALTER ROLE " + new_user + " SUPERUSER;")
con.commit()

cur.execute("CREATE EXTENSION postgres_fdw;")
con.commit()

cur.execute("GRANT ALL PRIVILEGES ON FOREIGN DATA WRAPPER postgres_fdw to " + new_user + " ;")
con.commit()


# Create foreign stuff for NOVA

cur.execute("CREATE SERVER foreign_server_nova " +
            "FOREIGN DATA WRAPPER postgres_fdw " +
            "OPTIONS (host %s, port '5432', dbname 'nova');", (_host,))
con.commit()

cur.execute("GRANT ALL PRIVILEGES ON foreign server foreign_server_nova to " + new_user + " ;")
con.commit()

cur.execute("CREATE USER MAPPING FOR " + new_user + " " +
            "SERVER foreign_server_nova " +
            "OPTIONS (user 'nova', password 'nova');")
con.commit()

cur.execute("CREATE FOREIGN TABLE foreign_nova ( " +
            "uuid char(36) NOT NULL, " +
            "hostname char(255) "
            ") " +
            "SERVER foreign_server_nova " +
            "OPTIONS (schema_name 'public', table_name 'instances', updatable 'false');")
con.commit()

cur.execute("GRANT ALL PRIVILEGES ON TABLE foreign_nova TO " + new_user + ";")
con.commit()



# Create foreign stuff for KEYSTONE
cur.execute("CREATE SERVER foreign_server_keystone " +
            "FOREIGN DATA WRAPPER postgres_fdw " +
            "OPTIONS (host %s, port '5432', dbname 'keystone');", (_host,))
con.commit()

cur.execute("GRANT ALL PRIVILEGES ON foreign server foreign_server_keystone to " + new_user + " ;")
con.commit()

cur.execute("CREATE USER MAPPING FOR " + new_user + " " +
            "SERVER foreign_server_keystone " +
            "OPTIONS (user 'keystone', password 'keystone');")
con.commit()

cur.execute("CREATE FOREIGN TABLE foreign_keystone ( " +
            "id char(64) NOT NULL, " +
            "name char(255) NOT NULL"
            ") " +
            "SERVER foreign_server_keystone " +
            "OPTIONS (schema_name 'public', table_name 'user', updatable 'false');")
con.commit()

cur.execute("GRANT ALL PRIVILEGES ON TABLE foreign_keystone TO " + new_user + ";")
con.commit()



# Create third table (one-to-one)
cur.execute("CREATE TABLE vm_user ( " +
            "vm_uuid char (36) NOT NULL UNIQUE," +
            "user_id char (64) NOT NULL UNIQUE);")
con.commit()

cur.close()
con.close()



