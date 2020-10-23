from nltk.tokenize import word_tokenize
import nltk
import mysql.connector

#nltk.download("punkt")

db = mysql.connector.connect(
    host = "devilberry.local",
    port = "3306",
    user = "grafana",
    password = "DB_R4CkG",
    database = "temperatura"
)

cursor = db.cursor()

f = open("oldlogsS.log", "r")
file = f.read()

words = word_tokenize(file)

for i in range(int(len(words)/6)):
    timestamp = int(words[i*6][0:10])
    temperature = float(words[i*6+1][5:])
    humidity = float(words[i*6+4][9:13])
    sql = "insert into lettura values (null, 5, "+str(temperature)+", "+str(humidity)+", "+str(timestamp)+");"
    cursor.execute(sql)
    db.commit()