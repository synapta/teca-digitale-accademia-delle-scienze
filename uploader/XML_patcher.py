from internetarchive.session import ArchiveSession
from internetarchive.search import Search
from internetarchive import get_item
from internetarchive import upload
import xml.etree.ElementTree as ET
from timeout import TimeoutError
from timeout import timeout
import internetarchive
import pandas as pd
import os

@timeout(10)
def bookDL(bookID):
    item.download(bookID+'_scandata.xml', destdir="./scandata_files/")

@timeout(20)
def bookUL(fid, file):
    return upload(fid, files=file)

#prepare files and folders
if not os.path.exists('./scandata_files/'):
    os.mkdir('./scandata_files/')
if not os.path.exists('./patched_files/'):
    os.mkdir('./patched_files/')
if not os.path.exists('./patched_files/patched_files.txt'):
    with open('./patched_files/patched_files.txt', "w") as f:
        f.write("file_ID\n")
if not os.path.exists('./patched_files/uploaded_files.txt'):
    with open('./patched_files/uploaded_files.txt', "w") as f:
        f.write("file_ID\n")

s = ArchiveSession()
search = Search(s, '(uploader:accademia.scienze.torino@synapta.it)')

#download
basedir = "./scandata_files/"
for result in search:
    id = result['identifier']
    if id in os.listdir(basedir):
        continue
    item = get_item(id)
    file = internetarchive.File(item, result['identifier']+'_scandata.xml')
    while True:
        try:
            bookDL(id)
        except TimeoutError:
            print("Timeout")
            continue
        break

basedir = "./scandata_files/"
patched_files = pd.read_csv("patched_files/patched_files.txt")['file_ID'].tolist()

#patch
for dir in os.listdir(basedir):
    if dir not in patched_files:
        print("Patching file with ID:",dir)
        file_path = basedir + "/" + dir + "/" + dir + "_scandata.xml"
        tree = ET.parse(file_path)
        root = tree.getroot()

        for index,page in enumerate(root.find('pageData').findall('page')):
            if page.find('pageNumber') is None:
                pnum = ET.SubElement(page, 'pageNumber')
                pnum.text = str(index+1)

        tree.write("patched_files/" + dir + "_scandata.xml")
        with open("patched_files/patched_files.txt", "a") as f:
            f.write(dir+"\n")

uploaded_files = pd.read_csv("patched_files/uploaded_files.txt")['file_ID'].tolist()

#upload
for dir in os.listdir(basedir):
    if dir not in uploaded_files:
        fname = dir + "_scandata.xml"
        file_path = "patched_files/" + fname
        print("Uploading file for ID:",dir)
        while True:
            try:
                res = bookUL(dir, file_path)
            except TimeoutError:
                print("Timeout")
                continue
            break
        code = res[0].status_code

        if code == 200:
            with open("patched_files/uploaded_files.txt", "a") as f:
                f.write(dir+"\n")
        else:
print("Upload failed with code", code)
