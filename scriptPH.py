import os
import json
import mysql.connector
import time

db = mysql.connector.connect(
    host = "devilberry.local",
    port = "3306",
    user = "grafana",
    password = "DB_R4CkG",
    database = "temperatura"
)
cursor = db.cursor()

stream = os.popen("curl http://192.168.1.15/api/JEVj-XKcmmzCEEElM44V2XumS7cPvjZ42p7X573Q")
output = stream.read()
js = json.loads(output)

sqlQuery = "select id_sen from sensore where mac=%s;"
sqlInsert = "insert into lettura values(NULL, %s, %s, NULL, %s);"
sqlUpdate = "update sensore set batteria=%s where id_sen=%s;"
val = list()

for sensor in js["sensors"].items():
    if(sensor[1]["type"] == "ZLLTemperature"):
        #print(sensor)
        #gets id_sen from 'mac'
        mac = sensor[1]["uniqueid"][15:23]
        val = [mac]
        cursor.execute(sqlQuery, val)
        id = cursor.fetchall()[0][0]
        
        batteria = sensor[1]["config"]["battery"]
        temperatura = sensor[1]["state"]["temperature"]/100.0
        #umidita = "NULL"
        timestamp = str(time.time())[0:10]
        #print(timestamp)

        #adds lettura
        val = [id, temperatura, timestamp]
        cursor.execute(sqlInsert, val)
        db.commit()

        #updates battery
        val = [batteria, id]
        cursor.execute(sqlUpdate, val)
        db.commit()

db.close()