import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import requests


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur

#find the average runtime for top movies each year
def runtimeByYear(cur): 
    d = {}
    for i in range(2001,2023):
        year_runtime = cur.execute("""SELECT AVG(runtime) FROM movies WHERE year = (?)""",
                                   (i,)).fetchone()[0]
        if year_runtime != None:
            # print(year_runtime)
            d[i] = round(year_runtime,2)
    # print(d)
    return d
    pass

#find the average runtime by genre
def runtimeByGenre(cur):
    d = {}
    total_genres = cur.execute("SELECT genre FROM Genres").fetchall()
    # print(total_genres)
    for i in range(len(total_genres)):
        current_genre = total_genres[i][0]
        # print(current_id,current_genre)
        genre_runtime = cur.execute("""SELECT AVG(movies.runtime) FROM Movies JOIN genres
        ON movies.genre1_id = genres.id  or movies.genre2_id = genres.id or movies.genre3_id = genres.id
        WHERE genres.genre = (?)""",(current_genre,)).fetchone()[0]
        d[current_genre] = round(genre_runtime,2)

    return d
        
def percentDif(data):
    d = {}
    items = list(data.items())
    for i in range(len(items)):
        pair = items[i]
        # print(pair[0])
        if i == 0:
            d[pair[0]] = 1
            pass
        # print(items[i])
        else:
            prev_pair = items[0]
            # prev_pair = items[i-1]
            dif = pair[1] - prev_pair[1]
            percentage = dif / (prev_pair[1])
            # print(percentage)
            d[pair[0]] = round(percentage,2) + 1

    # print(d)
    return d
    
    pass

#find the average score by rating
def scoreByRating(cur):
    d = {}
    total_ratings = cur.execute("SELECT rating from Ratings").fetchall()
    # print(total_ratings)
    for i in range(len(total_ratings)):
        current_rating = total_ratings[i][0]
        # print(current_rating)
        rating_score = cur.execute("""SELECT AVG(movies.metacritic_score) FROM Movies JOIN ratings
        ON movies.rating_id = ratings.id WHERE ratings.rating = (?)""",(current_rating,)).fetchone()[0]
        # print(rating_score)
        d[current_rating] = round(rating_score,2)

    return d

    pass


# plot runtime averages found for given years
def plotYear(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x_list = []
    y_list = []
    for year in data:
        x = year
        y = data[year]
        x_list.append(x)
        y_list.append(y)
        ax.scatter(x, y, color='k', linewidth=2)

    x_list = np.array(x_list)
    y_list = np.array(y_list)
    a, b = np.polyfit(x_list, y_list, 1)
    plt.plot(x_list, a*x_list+b, color='red')

    ax.set_xlabel("Year")
    ax.set_ylabel("Average Runtime")


    fig.savefig("Average_Runtime_by_Year")

    plt.show()
        
        
    pass

# plot year by percentage difference
def plotPercent(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x_list = []
    y_list = []
    for year in data:
        x = year
        y = data[year]
        x_list.append(x)
        y_list.append(y)
        ax.scatter(x, y, color='k', linewidth=2)

    x_list = np.array(x_list)
    y_list = np.array(y_list)
    a, b = np.polyfit(x_list, y_list, 1)
    plt.plot(x_list, a*x_list+b, color='blue')

    ax.set_xlabel("Year")
    ax.set_ylabel("Percent Change in Average Runtime")


    fig.savefig("Percent_Average_Runtime_by_Year")

    plt.show()
        
        
    pass

# plot runtime averages found for given genres
def plotGenre(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    for genre in data:
        x = genre
        y = data[genre]
        ax.barh(x, y, linewidth=2)

    ax.set_ylabel("Genre")
    ax.set_xlabel("Average Runtime")

    fig.savefig("Average_Runtime_by_Genre")

    plt.show()
    pass

# plot score averages for given ratings
def plotRating(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    for rating in data:
        x = rating
        y = data[rating]
        ax.bar(x, y, linewidth=2)

    ax.set_xlabel("Rating")
    ax.set_ylabel("Average Metacritic Score")

    fig.savefig("Average_Score_by_Rating")

    plt.show()
    pass


def writeData(data_l):
    final_d = {}
    ratings = ['PG','PG-13','G','R','Not Rated']
    final_d["year_data"] = {}
    for d in data_l:
        keys = list(d.keys())
        if type(keys[0]) == int:
            if d[keys[0]] == 1:
                final_d["year_data"]["percent_change"] = d
                pass
            else:
                final_d["year_data"]["avg_runtime"] = d
                pass
        else:
            if keys[0] in ratings:
                final_d["rating_score"] = d
                pass
            else:
                final_d["genre_runtime"] = d
                pass

    # print(final_d)
        
    with open("movies.json","w") as f:
        json.dump(final_d,f, indent=2)


    pass








def main():
    data_l = []
    cur = setUpDatabase("movies.db")
    year_d = runtimeByYear(cur)
    # print(year_d)
    data_l.append(year_d)
    percent_d = percentDif(year_d)
    data_l.append(percent_d)
    # plotPercent(percent_d)
    # plotYear(year_d)

    genre_d = runtimeByGenre(cur)
    # print(genre_d)
    data_l.append(genre_d)
    # plotGenre(genre_d)

    score_d = scoreByRating(cur)
    # print(score_d)
    data_l.append(score_d)
    # plotRating(score_d)

    # print(data_l)

    writeData(data_l)

    


    pass



main()


# List old resources we used such a HW's?  Don't need to
# Should all our calculations be written to one file?  Can be multiple
#Should one of the visualizations have data from both APIS? Try to have them include both

# Presentation Notes:
# Completely seperate data/visualizations, two seperate data files in presentation one
# put number of barchart on graph?
# make sure only 25 each time (probably just avoid driver file)

