# -*- coding: utf-8 -*-

import requests 
import pandas as pd
import os
import json
import xml.etree.ElementTree as ET
import pandas as pd
import time
from numpy import nan as Nan
from internetarchive import upload
import sys
import glob
#import shutil

if os.path.exists('./book.csv'):
    bookdf = pd.read_csv('book.csv', dtype=str, encoding='utf-8')
    done = bookdf['identifier'].tolist()
else:
    done = []

basedir = "/data/accademia/teca/storage/Asto/"
namespace = '{http://www.iccu.sbn.it/metaAG1.pdf}'
purl = '{http://purl.org/dc/elements/1.1/}'
counter = 0
data = []
for directory in os.listdir(basedir):
    print directory
    for element in os.listdir(basedir + '/' + directory):
        if ".xml" == element[-4:] and element.replace(".xml", "") not in done and 'Lotto' in directory:
            bookObj = {}
            part_name = ""

            filename = basedir + '/' + directory + '/' +  element

            tree = ET.parse(filename)
            root = tree.getroot()
            identifier = element.replace(".xml", "")
            bookObj['type'] = root.find('./' + namespace + 'bib').attrib['level']
            if bookObj['type'] == 'm':
                bookObj['type']  = 'Monografia'
            if bookObj['type'] == 's':
                bookObj['type']  = 'Periodico'
            
            for child in root.find(namespace+'bib'):

                if 'identifier' in child.tag:
                    bookObj['identifier'] = element.replace(".xml", "")
                elif 'title' in child.tag:
                    bookObj['title'] = child.text
                elif 'creator'in child.tag:
                    bookObj['creator'] = child.text
                elif 'publisher' in child.tag:
                    bookObj['publisher'] = child.text
                elif 'description' in child.tag:
                    bookObj['description'] = child.text
                elif 'date' in child.tag:
                    if 'date' not in bookObj.keys():
                        bookObj['date'] = child.text
                #elif 'format' in child.tag:
                #    bookObj['format'] = child.text
                elif 'language' in child.tag:
                    bookObj['language'] = child.text
                elif 'piece' in child.tag:
                    if child.find(namespace + 'part_name') is not None:
                        part_name = child.find(namespace + 'part_name').text
                    elif child.find(namespace + 'issue') is not None:
                        #print child.find(namespace + 'issue').text
                        part_name = child.find(namespace + 'issue').text

                if part_name != "":
                    bookObj['title'] = bookObj['title'] + " " + part_name

                
                bookObj['mediatype'] = 'texts'

            counter = counter + 1
            data.append(bookObj)

dump =  json.dumps(data, indent=4, sort_keys=True)            
print counter

with open('book.json', 'w') as f:
    f.write(dump)

"""
Per rimuovere la linea con il libro da ritentare
df = df[~df['your column'].isin(['list of strings'])]
"""
