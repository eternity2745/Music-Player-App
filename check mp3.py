import mysql.connector as mc
import os.path

con = mc.connect(host='localhost', user='root', database='musicplayer', password='')
cur = con.cursor()
cur.execute("select mp3 from songs")
q = cur.fetchall()
for i in q: 
    if os.path.isfile(i[0]) == False:
        print(i[0])
    

cur.close()
con.close()

    
