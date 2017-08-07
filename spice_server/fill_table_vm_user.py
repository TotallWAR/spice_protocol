import psycopg2

def add_user_instance ():
        vm_uuid=str(raw_input("Enter vm_uuid: "))
        user_id=str(raw_input("Enter user_id: "))
        try:
            broker_conn = psycopg2.connect(dbname="broker", user="broker", host="10.0.2.11", password="broker")
        except Exception as e:
            print e.message
        	# print "I am unable to connect to the database"
            broker_conn = None
            return e.message
        cur = broker_conn.cursor()
        cur.execute("SELECT uuid FROM foreign_nova WHERE uuid=%s;", (vm_uuid,))
        vm_uuid = cur.fetchone()
        
        cur.execute("SELECT id FROM foreign_keystone WHERE id=%s;", (user_id,))
        user_id = cur.fetchone()
        print("vm_uuid   " + str(vm_uuid) + " user_id " + str(user_id))
        if(vm_uuid and user_id):
            cur.execute("""INSERT INTO vm_user VALUES (%s,%s);""", (vm_uuid, user_id))
            broker_conn.commit()
            return True
        else:
            return None
        cur.close()
        broker_conn.close()
add_user_instance ()
