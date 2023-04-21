import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import re
import requests

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



def collectData(key, year, index):
    query = f"""https://imdb-api.com/API/AdvancedSearch/{key}?title_type=feature&release_date={year}-01-01,{year}-12-31&languages=en&count=100&sort=boxoffice_gross_us,desc"""
    # print(query)

    response = requests.get(query)


    data = json.loads(response.text)
    movies = data['results']
    data_l = []
    for i in range(index,index+25):
        movie = movies[i]
        id = movie['id'].strip()
        title = movie['title'].strip()
        year_search = re.findall("(\d{4})",movie['description'])
        year = year_search[0].strip()
        runtime = movie['runtimeStr'].strip("min").strip()
        # print(year)
        genres = movie['genres'].split(",")
        for i in range(3):
            if i >= len(genres):
                genres.append("N/A")
            else:
                genres[i] = genres[i].strip()
        # print(genres)
        rating = movie['contentRating']
        if rating:
            rating = rating.strip()
        meta_score = movie['metacriticRating']
        if meta_score:
            meta_score = meta_score.strip()
        data_l.append((id,title,year,runtime,genres,rating,meta_score))

    return data_l

def createTables(cur,conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS Movies
    (id TEXT PRIMARY KEY UNIQUE, title TEXT, year INTEGER, runtime INTEGER, genre1_id INTEGER, genre2_id INTEGER, genre3_id INTEGER, 
    rating_id INTEGER, metacritic_score INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Genres
    (id INTEGER PRIMARY KEY UNIQUE, genre TEXT UNIQUE)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Ratings
    (id INTEGER PRIMARY KEY UNIQUE, rating TEXT UNIQUE)""")

    conn.commit()


def updateSideTables(cur, conn, data_l):
    for data in data_l:
        # print(data)
        cur.execute("INSERT OR IGNORE INTO Ratings (rating) VALUES (?)",(data[-2],))
        for genre in data[-3]:
            cur.execute("INSERT OR IGNORE INTO Genres (genre) VALUES (?)",(genre,))

    conn.commit()
    pass

def updateMainTable(cur,conn,data_l):
    for data in data_l:
        genre_l = data[-3]
        # print(genre_l)
        genre1 = cur.execute("""SELECT id FROM Genres WHERE (?) = genre""",
                             (genre_l[0],)).fetchone()[0]
        genre2 = cur.execute("""SELECT id FROM Genres WHERE (?) = genre""",
                             (genre_l[1],)).fetchone()[0]
        genre3 =cur.execute("""SELECT id FROM Genres WHERE (?) = genre""",
                             (genre_l[2],)).fetchone()[0]
        genre_tup = (genre1,genre2,genre3)

        rating_id = cur.execute("""SELECT id FROM Ratings WHERE (?) = rating""",
                             (data[-2],)).fetchone()
        
        formatted_data = data[:4] + genre_tup + rating_id + data[6:]
        # print(formatted_data)

        cur.execute("""INSERT OR IGNORE INTO Movies (id, title, year, runtime, genre1_id, genre2_id, genre3_id, 
    rating_id, metacritic_score) VALUES (?,?,?,?,?,?,?,?,?)
        """,(formatted_data))

        conn.commit()







def main():
    api_key = "k_xsn1aztr"
    cur, conn = setUpDatabase("movies.db")
    createTables(cur, conn)
    while True:
        try:
            user_year = int(input("""Please input a year between 2001 and 2022 to add 25 movies from (type "-1" to end code). """))
            if user_year == -1:
                ("Ending Program")
                return None
            if user_year > 2000 and user_year < 2023:
                amount_from_year = cur.execute("""SELECT year FROM Movies WHERE
                year = (?)""",(user_year,)).fetchall()
                index = len(amount_from_year)
                if index > 75:
                    print("You have the maximum data for this year, choose another please")
                else:
                    year = user_year
                    break
            else:
                print("Invalid Year, please try again")
        except:

            print("Invalid Year, please try again")

    data_l = collectData(api_key, year, index)
    # data_l = collectData(api_key, 2018, 0)
    # print(data_l)

    updateSideTables(cur, conn, data_l)

    updateMainTable(cur,conn,data_l)



    pass



main()