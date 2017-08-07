# coding=utf-8
import socket
import re
import psycopg2
import broker_log as logg
from novaclient import client
from config import *
srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvsock.bind((LISTEN_IP, 23005))
srvsock.listen(5)
print("Server Up")


def check_user(username):
    try:
        broker = psycopg2.connect(dbname="broker",
                                  user="broker", host=DB_IP,
                                  password="broker")
    except Exception as e:
        print e.message
        # print "I am unable to connect to the database"
        broker = None
        return e.message
    cur = broker.cursor()
    cur.execute("""SELECT id from foreign_keystone where name = %s;""",
                (username,))
    user_id = cur.fetchone()
    cur.close()
    broker.close()
    if(user_id):
        return user_id[0]
    else:
        return None
while True:
    clisock, (remhost, remport) = srvsock.accept()
    rq = clisock.recv(100).decode("utf-8")
    if (rq is not None):
        print("Client " + str(remhost) + "with port" +
              str(remport) + " try connect\n")
    user_creds = re.split(" ", rq)
    user_id = check_user(user_creds[0])
    if (user_id is not None):
        broker = psycopg2.connect(dbname="broker", user="broker",
                                  host=DP_IP, password="broker")
        cur = broker.cursor()
        cur.execute("""SELECT vm_uuid from vm_user where user_id = %s;""",
                    (user_id,))
        vm_uuid = cur.fetchone()
        if (vm_uuid is not None):
            cur.execute("""SELECT hostname from foreign_nova
                       where uuid = %s;""", (vm_uuid[0],))
            vm_name = cur.fetchone()
            print("username: " + user_creds[0] + "\nvm_uuid: " + vm_uuid[0])
            nova = client.Client("2",
                                 auth_url='http://controller:5000/v2.0',
                                 username=user_creds[0],
                                 api_key=user_creds[1],
                                 project_id='admin')
            try:
                server = nova.servers.get(vm_uuid[0])
            except Exception as e:
                clisock.send(e.message)
                logg.log(e.message)
            else:
                clisock.send(server.get_spice_console
                             ('spice-html5')['console']['url'])
                logg.log("User " + user_creds[0] +
                         " has get access for VM: " + vm_name[0])
        else:
            clisock.send("204")
            logg.log("ERROR 204 user doesnt have vm. Table vm_user doesnt have such user")
    else:
        clisock.send("401")
        logg.log("ERROR 401 No Content. Ther is not such user")


clisock.close()
del clisock
print ("Server Down")
