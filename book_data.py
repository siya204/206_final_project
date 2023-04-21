import sqlite3

# Open a connection to the database
conn = sqlite3.connect('final.db')
c = conn.cursor()

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

# Set a counter to keep track of how many books have been processed
counter = 0

# Loop through each book in the section and extract the title, author, and rating
for book in books_section.find_all("tr", {"itemtype": "http://schema.org/Book"}):
    if counter == 700:
        break
    
    # Extract the title of the book
    title = book.find("a", {"class": "bookTitle"}).text.strip()

    # Extract the link to the book page
    link = "https://www.goodreads.com" + book.find("a", {"class": "bookTitle"}).get("href")

    # Extract the author of the book
    author = book.find("a", {"class": "authorName"}).text.strip()
    
    # Extract the rating of the book
    rating = book.find("span", {"class": "minirating"}).text.strip().split()[0]
    
    try:
        ratings.append(float(rating))
        titles.append(title)
        authors.append(author)
    except:
        continue
    
    # Increment the counter
    counter += 1
    
    # Write to the database every 25 entries
    if counter % 25 == 0:
        data = list(zip(titles, authors, ratings))
        c.executemany('INSERT INTO book_ratings (title, author, rating) VALUES (?, ?, ?)', data)
        conn.commit()
        titles.clear()
        authors.clear()
        ratings.clear()

# Write any remaining entries to the database
if titles:
    data = list(zip(titles, authors, ratings))
    c.executemany('INSERT INTO book_ratings (title, author, rating) VALUES (?, ?, ?)', data)
    conn.commit()
    titles.clear()
    authors.clear()
    ratings.clear()

# Close the database connection
conn.close()
