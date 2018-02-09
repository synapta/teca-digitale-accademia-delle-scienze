import pandas as pd
import os
import xml.etree.ElementTree as ET
import pandas as pd
from numpy import nan as Nan

basedir = "/data/davide/accademia/teca/storage/Asto"
namespace = '{http://www.iccu.sbn.it/metaAG1.pdf}'
purl = '{http://purl.org/dc/elements/1.1/}'

data = pd.DataFrame()
#columns=['date', 'date0', 'coverage', 'creator', 'coverage', 'credits', 'description', 'language', 'licenseurl', 'mediatype'])


for directory in os.listdir(basedir):
    print directory
    for element in os.listdir(basedir + '/' + directory):
        if ".xml" == element[-4:]:

            bookObj = {}
            filename = basedir + '/' + directory + '/' +  element
            tree = ET.parse(filename)
            root = tree.getroot()

            for child in root.find(namespace+'bib'):
                if child.tag == purl+'identifier':
                    bookObj['identifier'] = [element.replace(".xml", "")]
                elif child.tag == purl+'title':
                    bookObj['title'] = [child.text]
                elif child.tag == purl+'creator':
                    bookObj['creator'] = [child.text]
                elif child.tag == purl+'publisher':
                    bookObj['publisher'] = [child.text]
                elif child.tag == purl+'description':
                    bookObj['description'] = [child.text]
                elif child.tag == purl+'date':
                    if 'date' not in bookObj.keys():
                        bookObj['date[0]'] = [child.text]
                    else:
                        bookObj['date[1]'] = [child.text]
                elif child.tag == purl+'format':
                    bookObj['format'] = [child.text]
                elif child.tag == purl+'language':
                    bookObj['language'] = [child.text]

        bookDf = pd.DataFrame(bookObj)
        data = data.append(bookDf)

data.to_csv('book.csv',encoding='utf8')



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
"""
