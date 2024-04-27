# Mark Haddad
# CS 4250
# parser.py

from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

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

#collections
pages = db.pages
professors = db.professors

facultyURL = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"

def parseFaculty():
    result = pages.find(filter={"url": facultyURL}, projection={"html":1, "_id":0})
    html = result[0]["html"]
    bs = BeautifulSoup(html, 'html.parser')
    faculty = bs.find_all('div', {'class': 'clearfix'})

    for member in faculty:
        name = member.find('h2')
        if name:
            name = name.get_text()
            title = member.find('strong', string=re.compile('^.*Title.*$')).next_sibling.get_text()
            office = member.find('strong', string=re.compile('^.*Office.*$')).next_sibling.get_text()
            phone = member.find('strong', string=re.compile('^.*Phone.*$')).next_sibling.get_text()
            email = member.find('strong', string=re.compile('^.*Email.*$')).find_next('a').get('href').split(':')[1]
            website = member.find('strong', string=re.compile('^.*Web.*$')).find_next('a').get('href')
            print(name, title, office, phone, email, website)

            faculty_member = {
                'name': name,
                'title': title,
                'office': office,
                'phone': phone,
                'email': email,
                'website': website
            }

            professors.insert_one(faculty_member)

def main():
    parseFaculty()

if __name__ == "__main__":
    main()