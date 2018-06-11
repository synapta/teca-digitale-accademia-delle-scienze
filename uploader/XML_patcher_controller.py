from timeout import timeout
import internetarchive
from internetarchive.session import ArchiveSession
from internetarchive.search import Search
from internetarchive import upload
from internetarchive import get_item
import xml.etree.ElementTree as ET
import os
import pandas as pd

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
if not os.path.exists(dest_dir+'patched_files.txt'):
    with open(dest_dir+'patched_files.txt', "w") as f:
        f.write("file_ID\n")
if not os.path.exists(dest_dir+'uploaded_files.txt'):
    with open(dest_dir+'uploaded_files.txt', "w") as f:
        f.write("file_ID\n")

s = ArchiveSession()
search = Search(s, '(uploader:accademia.scienze.torino@synapta.it)')

#download
count = 1
for result in search:
    print(count)
    count+=1
    id = result['identifier']
    if id in os.listdir(base_dir):
        continue
    item = get_item(id)
    file = internetarchive.File(item, result['identifier']+'_scandata.xml')
    while True:
        try:
            bookDL(id)
        except Exception as ex:
            continue
        break

patched_files = pd.read_csv("patched_files_all/patched_files.txt")['file_ID'].tolist()

#patch
for dir in os.listdir(base_dir):
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
        with open(dest_dir+"patched_files.txt", "a") as f:
            f.write(dir+"\n")

uploaded_files = pd.read_csv("patched_files_all/uploaded_files.txt")['file_ID'].tolist()
patched_files = pd.read_csv("patched_files_all/patched_files.txt")['file_ID'].tolist()

#upload
for file in patched_files:
    fname = dest_dir + file + "/" + file + "_scandata.xml"
    print("Uploading file for ID:",fname)
    while True:
        try:
            res = bookUL(dir, file_path)
        except Exception as ex:
            print(ex)
            continue
        break
    code = res[0].status_code

    if code == 200:
        with open("patched_files/uploaded_files.txt", "a") as f:
            f.write(dir+"\n")
    else:
        print("Upload failed with code", code)
