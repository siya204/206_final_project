import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


# Define the URL of the Goodreads top 250 books page
url = "https://www.goodreads.com/list/show/1.Best_Books_Ever"


# Make a GET request to the URL and parse the HTML content using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the section of the page that contains the book titles and links
books_section = soup.find("table", {"class": "tableList"})


# Create empty lists to store the titles, authors and ratings
titles = []
authors = []
ratings = []

count = 0
# Loop through each book in the section and extract the title and link
for book in books_section.find_all("tr", {"itemtype": "http://schema.org/Book"}):
    if count == 700 :
        break
    
    # Extract the title of the book
    title = book.find("a", {"class": "bookTitle"}).text.strip()

    # Extract the link to the book page
    link = "https://www.goodreads.com" + book.find("a", {"class": "bookTitle"}).get("href")

    # Extract the author of the book
    author = book.find("a", {"class": "authorName"}).text.strip()
    
    # Extract the rating of the book
    rating = book.find("span", {"class": "minirating"}).text.strip().split()[0]
    
    try :
        ratings.append(float(rating))
        titles.append(title)
        authors.append(author)
        
    except :
        continue
        
    count += 1



# Making sure that all the lists are of the same length
len(titles), len(authors), len(ratings)

# Create a dataframe using the lists
df = pd.DataFrame(data={'Author':authors, 'Title':titles,'Rating':ratings})

# Get list of the top 5 authors
top5authors = df.groupby('Author')['Rating'].mean().reset_index()
top5authors

# Create a bar chart of the ratings
fig, ax = plt.subplots()
ax.bar(top5authors['Author'][:5], top5authors['Rating'][:5])
ax.set_title("Top-Rated Authors")
ax.set_xlabel("Author")
ax.set_ylabel("Rating")
plt.subplots_adjust(bottom=0.4)
plt.xticks(rotation=90)
plt.show()

# Create a scatter plot to visualize the relationship between the book ratings and their authors.
fig, ax = plt.subplots()
ax.scatter(top5authors['Author'][:10], top5authors['Rating'][:10])
ax.set_title("Book Ratings by authors")
ax.set_xlabel("Author")
ax.set_ylabel("Rating")
plt.subplots_adjust(bottom=0.5)
plt.xticks(rotation=90)
plt.show()

# Create a box plot of the ratings
fig, ax = plt.subplots()
ax.boxplot(df['Rating'])
ax.set_title("Distribution of Book Ratings")
ax.set_ylabel("Rating")
plt.show()

#top10 = top10authors['Author'][:10].tolist()
#top10 = df[df['Author'].isin(top10)]

#authors = top10['Author'].tolist()
#titles = top10['Title'].tolist()
#ratings = top10['Rating'].tolist()

# Create a dictionary to store the ratings for each book
book_ratings = {}
for i in range(len(titles)):
    book_ratings[titles[i]] = ratings[i]


# Create a heatmap of the ratings for each book
fig, ax = plt.subplots()
ratings_matrix = np.zeros((len(titles), 1))
for i, title in enumerate(titles):
    ratings_matrix[i, 0] = book_ratings[title]
im = ax.imshow(ratings_matrix, cmap="Reds")
ax.set_xticks([])
ax.set_yticks(range(len(titles)))
ax.set_yticklabels(titles)
ax.set_title("Book Ratings")
fig.colorbar(im)
plt.show()



