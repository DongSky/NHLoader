import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import zipfile
import pathlib
import re

class Book(object):
    def __init__(self, book_id):
        self.id = book_id
        self.link = "https://nhentai.net/g/%d/" % int(book_id)
        self.grab()
    def grab(self):
        self.spider = requests.get(self.link)
        # print(self.spider.text)
        dict_reg = re.compile("gallery\(.+?\);")
        result_set = re.findall(pattern=dict_reg,string=self.spider.text)
        info_str = result_set[0].split("gallery(")[1].split(");")[0]
        self.info = eval(info_str)
        del info_str
        # print(self.info)
        self.title = self.info["title"]["japanese"]
        self.title_eng = self.info["title"]["english"]
        self.media_id = int(self.info["media_id"])
        self.thumb_link = "https://i.nhentai.net/galleries/%d/%d.jpg" % (self.media_id, 1)
        self.num = self.info["num_pages"]
        self.language = []
        self.parody = []
        self.tags = []
        self.character = []
        self.author = []
        self.group = []
        self.category = []
        for son in self.info["tags"]:
            if son["type"] == "parody":
                self.parody.append(son["name"])
            elif son["type"] == "language":
                self.language.append(son["name"])
            elif son["type"] == "tag":
                self.tags.append(son["name"])
            elif son["type"] == "character":
                self.character.append(son["name"])
            elif son["type"] == "group":
                self.group.append(son["name"])
            elif son["type"] == "category":
                self.category.append(son["name"])
            elif son["type"] == "artist":
                self.author.append(son["name"])

    def print_summary(self):
        print("e-Book id:/t", self.id)
        if self.title != "":
            print("Japanese Title:/t", self.title)
            print("English Title:/t", self.title_eng)
            print("pages:/t", self.num)
        if len(self.language) > 0:
            print("Language:/t",", ".join(self.language))
        if len(self.category) > 0:
            print("Category:/t",", ".join(self.category))
        if len(self.tags) > 0:
            print("Tags:/t",", ".join(self.tags))
        if len(self.character) > 0:
            print("Characters:/t",", ".join(self.character))
            if len(self.parody) > 0:
                print("Parody:/t",", ".join(self.parody))
        if len(self.author) > 0:
            print("Author:/t",", ".join(self.author))
        if len(self.group) > 0:
            print("Group:/t",", ".join(self.group))

    def download_all(self):
        download_path = os.getcwd() + "/download/" + str(self.id) + "/"
        if not os.path.exists(str(download_path)):
            os.makedirs(str(download_path))
            print("Downloading: %s"%self.title)
            try:
                for idx in tqdm(range(1, self.num+1)):
                    suffix = "jpg"
                    cur_img_link = "https://i.nhentai.net/galleries/%d/%d.%s" % (self.media_id, idx, suffix)
                    res = requests.get(cur_img_link).content
                    try:
                        if len(res) < 1024:
                            suffix = "png"
                            cur_img_link = "https://i.nhentai.net/galleries/%d/%d.png" % (self.media_id, idx)
                            res = requests.get(cur_img_link).content 
                    except Exception as e:
                        print(e)
                    img_path = download_path + str("%d.%s"%(idx, suffix))
                    with open(img_path,"wb") as f:
                        f.write(res)
                        f.close()
                print("%s downloaded."%self.title_eng)
                print("Path: %s"%str(download_path))
            except Exception as e:
                print(e)

    def pack(self):
        download_path = str("download/" + str(self.id) + "/")
        zip_file_path = str("download/" + str(self.id)+".zip")
        try:
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as f:
                for dirPath, dirNames, fileNames in os.walk(download_path):
                    for filename in fileNames:
                        f.write(os.path.join(dirPath, filename))
                    f.close()
                return zip_file_path
        except Exception as e:
            print(e)
            return None
