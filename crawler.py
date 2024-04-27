# Mark Haddad
# CS 4250
# crawler.py

from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.error import HTTPError
from urllib.error import URLError

def connectDataBase():

    DB_NAME = "assignment4"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db
    except:
        print("Database not connected successfully")

# database
db = connectDataBase()

# collection
pages = db.pages

url = 'https://www.cpp.edu/sci/computer-science/'
frontier = []
visited = []
frontier.append(url)

def crawlerThread(frontier):
    while frontier:
        url = frontier.pop(0)
        try:
            html = urlopen(url)
            html = html.read()
        except HTTPError as e:
            print(e)
        except URLError as e:
            print("The server could not be found!")
        bs = BeautifulSoup(html, 'html.parser')
        visited.append(url)
        html_data = html.decode('utf-8')

        document = {
                "url": url,
                "html": html_data
            }
        
        pages.insert_one(document)

        if bs.find("h1").get_text() == "Permanent Faculty":
            frontier.clear()
            print("Page Found")
        else:
            print("Crawling...")
            links = bs.find_all('a', href=True)
            for link in links:
                next_link = link['href']

                next_url = urljoin(url, next_link)

                if next_link not in visited:
                    frontier.append(next_url)

def main():
    crawlerThread(frontier)

if __name__ == "__main__":
    main()