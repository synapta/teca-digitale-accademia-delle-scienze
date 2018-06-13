from internetarchive.session import ArchiveSession
from internetarchive.search import Search
import xml.etree.ElementTree as ET
from internetarchive import get_item
from internetarchive import upload
from timeout import TimeoutError
from timeout import timeout
import internetarchive
import pandas as pd
import os

@timeout(10)
def bookDL(bookID):
    item.download(bookID+'_scandata.xml', destdir="./scandata_files_all/")

@timeout(20)
def bookUL(fid, file):
    return upload(fid, files=file)

base_dir = "./scandata_files_all/"
dest_dir = "./patched_files_all/"
#prepare files and folders
if not os.path.exists(base_dir):
    os.mkdir(base_dir)
if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)

#get all books uploaded by ASTO
s = ArchiveSession()
search = Search(s, '(uploader:accademia.scienze.torino@synapta.it)')

#download
count = 1
for result in search:
    print(count)
    count+=1
    id = result['identifier']
    item = get_item(id)
    file = internetarchive.File(item, result['identifier']+'_scandata.xml')
    while True:
        try:
            bookDL(id)
        except TimeoutError:
            print("Timeout")
            continue
        break

#patch
patched_files = []
for dir in os.listdir(base_dir):
    if dir not in patched_files:
        print("Patching file with ID:",dir)
        file_path = base_dir + "/" + dir + "/" + dir + "_scandata.xml"
        tree = ET.parse(file_path)
        root = tree.getroot()
        patched = False

        for index,page in enumerate(root.find('pageData').findall('page')):
            if page.find('pageNumber') is None:
                pnum = ET.SubElement(page, 'pageNumber')
                pnum.text = str(index+1)
                patched = True

        if patched:
            tree.write(dest_dir + dir + "_scandata.xml")
            patched_files.append(dir)

#upload
for file in patched_files:
    fname = dest_dir + file + "/" + file + "_scandata.xml"
    print("Uploading file for ID:",fname)
    while True:
        try:
            res = bookUL(dir, file_path)
        except TimeoutError:
            print("Timeout")
            continue
        break
    code = res[0].status_code

    if code != 200:
        print("Upload failed with code", code)
