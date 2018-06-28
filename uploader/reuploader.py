# -*- coding: utf-8 -*-

import requests
import pandas as pd
import os
import xml.etree.ElementTree as ET
import pandas as pd
from numpy import nan as Nan
from internetarchive import upload
import sys
import requests
import glob
import time
import ASTOteca



basedir = sys.argv[1]
namespace = '{http://www.iccu.sbn.it/metaAG1.pdf}'
purl = '{http://purl.org/dc/elements/1.1/}'

bookdf = pd.DataFrame()

data = []
for directory in os.listdir(basedir):
    print directory
    for element in os.listdir(basedir + '/' + directory):
        if ".xml" == element[-4:] and element.replace(".xml", "") and 'Stampa' in directory:
            done = False
            print element.replace(".xml", "")
            while done == False:
                try:
                    time.sleep(1)
                    r = requests.get("https://archive.org/metadata/" +  element.replace(".xml", ""), timeout=2)
                    done = True
                except:
                    done = False
                    print("Failed request")

            if r.text != '{}':
                print("skipping " + element.replace(".xml", ""))

            else:
                bookObj = {}
                part_name = ""
                filename = basedir + '/' + directory + '/' +  element

                bookObj = ASTOteca.parseXML(filename)

                print basedir + directory +  '/' + element.replace(".xml", "") + '/Archivio/'
                if os.path.exists(basedir + directory +  '/' + element.replace(".xml", "") + '/Archivio/'):
                    print "Compressing"
                    zip_exit_code = os.system('zip -r -j ' + bookObj['identifier'] + '_images.zip ' + basedir.replace(' ', '\ ') + directory.replace(' ', '\ ') +  '/' + element.replace(".xml", "") + '/Archivio/*')
                    #sys.exit(0)
                    if zip_exit_code != 0:
                        print "ERROR in creating the pdf. Exit code is: " + str(zip_exit_code)
                        sys.exit(zip_exit_code)

                    print "Uploading"
                    #print bookObj
                    del bookObj['toc']
                    del bookObj['cover_img']
                    code = -1
                    while code != 200:
                        try:
                            #print bookObj
                            r = upload(bookObj['identifier'],files=bookObj['identifier'] + '_images.zip', metadata=bookObj)
                            code = r[0].status_code
                        except:

                            print "Failed upload"

                    print "Done with code " + str(code)
                    bookObj['resCode'] = code

                    #shutil.copytree(filename.replace(".xml","") + '/Internet/', filename.replace(".xml","") + /bookObj['identifier'])
                    #print bookObj['identifier']
                    #sys.exit(0)
                    data.append(bookObj)
                    thisbookdf = pd.DataFrame(data)
                    bookdf = bookdf.append(thisbookdf, ignore_index=True)
                    bookdf.to_csv('uploading-debug-book.csv', index=False, encoding='utf-8')
