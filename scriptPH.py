import os
import json
import mysql.connector

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
sqlInsert = "insert into lettura values(%s, %s, %s, %s);"
sqlUpdate = "update sensore set batteria=%s where id_sen=%s;"
val = list()

for sensor in js["sensors"].items():
    if(sensor[1]["type"] == "ZLLTemperature"):
        #print(sensor)
        mac = sensor[1]["uniqueid"][15:23]
        val = [mac]
        cursor.execute(sqlQuery, val)
        id = cursor.fetchall()[0][0]
        
        batteria = sensor["config"]["battery"]
        temperatura = sensor["state"]["temperature"]
        val = []