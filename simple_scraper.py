from time import sleep
from selenium import webdriver
import sys
import sqlite3

class SimpleScraper:
    def __init__(self):
        self.urls = []
        self.db = sqlite3.connect("cache.db")
        self.cursor = self.db.cursor()

        result = self.cursor.execute("SELECT name FROM sqlite_master WHERE name='cache'")
        if result.fetchone() is None:
            self.cursor.execute("CREATE TABLE cache ( url TEXT, body TEXT, PRIMARY KEY( url ) )")
            self.db.commit()
        
        self.driver = webdriver.Firefox()

    def run(self, url_str, callback):
        self.addURL(url_str)

        while len(self.urls) > 0:
            current_url = self.urls.pop(0)
            self.driver.get(current_url)
            
            sleep(3)

            self.driver.maximize_window()
            
            sleep(1)

            data = (current_url, self.driver.page_source)
            self.cursor.execute("INSERT OR REPLACE INTO cache VALUES (? , ?)", data)
            self.db.commit()

            callback(self)

    def addURL(self, url_str):
        self.urls.append(url_str)

    def close(self):
        self.driver.close()
        self.db.close()

def callback(scraper):
    print(scraper.driver.title)

scraper = SimpleScraper()

scraper.addURL("https://www.bing.com")
scraper.run("https://duckduckgo.com/", callback)

scraper.close()