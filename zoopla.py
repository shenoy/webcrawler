import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import time


def homes(location):
    # request url
    index = 1
    homelist = []

    while index:
        print(index, "index is")
        base_url = f"https://www.zoopla.co.uk/for-sale/flats/{location}/?identifier={location.lower()}&property_type=flats&q={location}&radius=0&page_size=25&"
        url = f"pn={index}"
        print(url, url)
        response = requests.get(f"{base_url}{url}")
        soup = BeautifulSoup(response.text, "html.parser")        
        homes = soup.find_all(class_="listing-results-price text-price")
        count=0
        for home in homes:
	        count+=1
	        print("Entering for loop")
	        id = home["href"]
	        price = re.sub(r"[^\d]", "", home.get_text())
	        tup = (id, price)
	        homelist.append(tup)
        next_btn = soup.find(class_="paginate bg-muted").get_text() 
        next = next_btn.find('Next')
        print("sleeping 5 seconds")
        time.sleep(5)
        if next>1:
        	print("found Next Button")
        	index+=1
        else:
        	print("not found Next Button. Breaking from while loop....")       
        	index=0
        

    print(homelist, len(homelist))

    connection = sqlite3.connect(f"{location}.db")
    c = connection.cursor()
    c.execute(''' CREATE TABLE homes (id TEXT, price TEXT)''')
    c.executemany("INSERT INTO homes VALUES (?,?)", homelist)
    connection.commit()
    connection.close()


homes("Kent")
