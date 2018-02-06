import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import pathlib
import re
from Book import Book
class NHentai(object):
    def __init__(self):
        self.index_spider = requests.get("https://nhentai.net")
        self.random_spider = object
        self.parser = BeautifulSoup(self.index_spider.text, "html.parser")
    def refresh_index(self):
        self.index_spider = requests.get("https://nhentai.net")
        self.parser = BeautifulSoup(self.index_spider.text, "html.parser")
    def refresh_random(self):
        self.random_spider = requests.get("https://nhentai.net/random/")
        rand_id = int(self.random_spider.url.split("/")[-2])
        return Book(book_id=rand_id)
    def get_book(self, book_id):
        return Book(book_id)
    def search(self, query, is_popular):
        query_link = "https://nhentai.net/search/?q=%s"%query + ("&sort=popular" if is_popular else "")
        print(query_link)
        query_spider = requests.get(query_link)
        parser = BeautifulSoup(query_spider.text, "html.parser")
        body = parser.find_all("div", attrs={"class":"gallery"})
        for div in body:
            try:
                img_link = div.a.img["data-src"]
            except:
                img_link = div.a.img["src"]
            title = div.a.div.string
            _id = int(img_link.split("/")[-2])
            print(_id, title)
    def print_index(self):
        body = self.parser.find_all("div", attrs={"class":"gallery"})
        for div in body:
            try:
                img_link = div.a.img["data-src"]
            except:
                img_link = div.a.img["src"]
            title = div.a.div.string
            _id = int(img_link.split("/")[-2])
            print(_id, title)
if __name__ == "__main__":
    nh = NHentai()
    rand_book = nh.refresh_random()
    rand_book.download_all()
