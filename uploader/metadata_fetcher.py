# -*- coding: utf-8 -*-

import pandas as pd
import os
import xml.etree.ElementTree as ET
import pandas as pd
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

basedir = "/media/davide/Volume/ASTO/"
namespace = '{http://www.iccu.sbn.it/metaAG1.pdf}'
purl = '{http://purl.org/dc/elements/1.1/}'

data = []
#columns=['date', 'date0', 'coverage', 'creator', 'coverage', 'credits', 'description', 'language', 'licenseurl', 'mediatype'])


for directory in os.listdir(basedir):
    print directory
    for element in os.listdir(basedir + '/' + directory):
        if ".xml" == element[-4:] and element.replace(".xml", "") not in done:
            #and 'TO01157391_TO0324_62137_000000' in element:
            #print 'uploading'

            bookObj = {}
            part_name = ""

            filename = basedir + '/' + directory + '/' +  element

            tree = ET.parse(filename)
            root = tree.getroot()
            identifier = element.replace(".xml", "")
            print "Creating pdf for " + identifier

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

            zip_exit_code = os.system('zip -r ' + identifier + '_images.zip ' + basedir + directory.replace(' ', '\ ') +  '/' + element.replace(".xml", "") + '/Archivio/*')
            #sys.exit(0)
            if zip_exit_code != 0:

                print "ERROR in creating the pdf. Exit code is: " + str(convert_code)
                sys.exit(convert_code)

            print "Uploading"
            #print bookObj
            r = upload(bookObj['identifier'],files=identifier + '_images.zip', metadata=bookObj)

            code = r[0].status_code

            if code != 200:
                print "ERROR uploading with code: " + str(code)
                sys.exit(code)

            print "Done"
            bookObj['resCode'] = code

            #shutil.copytree(filename.replace(".xml","") + '/Internet/', filename.replace(".xml","") + /bookObj['identifier'])
            #print bookObj['identifier']
            #sys.exit(0)
            data.append(bookObj)
            thisbookdf = pd.DataFrame(data)
            bookdf = bookdf.append(thisbookdf, ignore_index=True)
            bookdf.to_csv('book.csv', index=False, encoding='utf-8')

"""
{http://purl.org/dc/elements/1.1/}publisher
{http://purl.org/dc/elements/1.1/}description
{http://purl.org/dc/elements/1.1/}date
{http://purl.org/dc/elements/1.1/}format
{http://purl.org/dc/elements/1.1/}language
{http://www.iccu.sbn.it/metaAG1.pdf}holdings
{http://www.iccu.sbn.it/metaAG1.pdf}piece
{http://purl.org/dc/elements/1.1/}identifier
{http://purl.org/dc/elements/1.1/}title
{http://purl.org/dc/elements/1.1/}creator
{http://purl.org/dc/elements/1.1/}publisher
{http://purl.org/dc/elements/1.1/}description
{http://purl.org/dc/elements/1.1/}date
{http://purl.org/dc/elements/1.1/}format
{http://purl.org/dc/elements/1.1/}language
{http://www.iccu.sbn.it/metaAG1.pdf}holdings


 * Part 1 | THIS WORLD | 1
 ** Chapter 1 | Of the Nature of Flatland | 3
 ** Chapter 2 | Of the Climate and Houses in Flatland | 5
 * Part 2 | OTHER WORLDS | 42


"""
