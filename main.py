from Book import Book
from NHentai import NHentai
import os
from tqdm import tqdm
import pathlib
import re
import requests
from bs4 import BeautifulSoup
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",action="store",type=str,help="search argument, input keywords, separate with exactly one +",dest="search")
    parser.add_argument("-p",action="store_true",default=False,help="popular search flag, only useful in search",dest="is_popular")
    parser.add_argument("-n",action="store",type=int,help="check manga with book id",dest="id")
    parser.add_argument("-d",action="store",default=False,help="download flag, valid with -n and -r",dest="is_download")
    parser.add_argument("-r",action="store_true",default=False,dest="random")
    flags = parser.parse_args()

    assert ((not flags.search is None) or (not flags.id is None))
    nhentai = NHentai()
    if flags.random:
        book = nhentai.refresh_random()
        if flags.is_download:
            book.print_summary()
            book.download_all()
        else:
            book.print_summary()
    elif not flags.id is None:
        book = nhentai.get_book(flags.id)
        if flags.is_download:
            book.print_summary()
            book.download_all()
        else:
            book.print_summary()
    elif not flags.search is None:
        nhentai.search(query=flags.search,is_popular=flags.is_popular)
