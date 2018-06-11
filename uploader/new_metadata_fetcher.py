# -*- coding: utf-8 -*-
import pandas as pd
import os
import xml.etree.ElementTree as ET
import sys
import pprint
import ASTOteca

if os.path.exists('./book.csv'):
    bookdf = pd.read_csv('book.csv', dtype=str, encoding='utf-8')
    done = bookdf['identifier'].tolist()
else:
    done = []

basedir = sys.argv[1]

data = []

for directory in os.listdir(basedir):
    print directory
    for element in os.listdir(basedir + '/' + directory):
        if ".xml" == element[-4:] and element.replace(".xml", "") not in done:

            filename = basedir + '/' + directory + '/' +  element
            bookInfo = ASTOteca.parseXML(filename)
            bookInfo["identifier"] = element.replace(".xml", "")

            data.append(bookInfo)


thisbookdf = pd.DataFrame(data)
if not os.path.exists("./book.csv"):
    bookdf = thisbookdf
else:
    bookdf = bookdf.append(thisbookdf, ignore_index=True)
bookdf.to_csv('book2.csv', index=False, encoding='utf-8')
