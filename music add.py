import mysql.connector as mc

con = mc.connect(host='localhost', user='root', database='musicplayer', password='')
cur = con.cursor()

while True:
    try:
        name = input("Enter song title: ")
        author = input("Enter song author: ")
        image = input("Song image: ")
        image = f"images/{image}"
        mp3 = f"music/{name}.mp3"
        lang = "tamil"
        genre = input("Song genre: ")

        cur.execute("INSERT INTO songs (title, author, image, mp3, language, genre) VALUES ('%s', '%s', '%s', '%s', '%s','%s')"%(name,author,image,mp3,lang,genre))
        con.commit()

    except Exception as e:
        print(e)

    finally:
        ch = input("Continue?: ")
        if ch in "Nn":
            cur.close()
            con.close()
            break
        else:
            continue

    
