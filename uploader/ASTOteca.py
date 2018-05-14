import pandas as pd
import timeout
import os
import xml.etree.ElementTree as ET

namespace = '{http://www.iccu.sbn.it/metaAG1.pdf}'
w3cns = '{http://www.w3.org/TR/xlink}'

def parseXML(file_path):
    bookObj = {}
    part_name = ""

    tree = ET.parse(file_path)
    root = tree.getroot()

    for child in root.find(namespace+'bib'):
        """if 'identifier' in child.tag:
            bookObj['identifier'] = element.replace(".xml", "")"""
        if 'title' in child.tag:
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
        elif 'language' in child.tag:
            bookObj['language'] = child.text
        elif 'piece' in child.tag:
            if child.find(namespace + 'part_name') is not None:
                part_name = child.find(namespace + 'part_name').text
            elif child.find(namespace + 'issue') is not None:
                part_name = child.find(namespace + 'issue').text

        if part_name != "":
            bookObj['title'] = bookObj['title'] + " " + part_name

        bookObj['mediatype'] = 'texts'

    #table of contents
    toc = {"toc":[]}
    for stru_elem in root.findall(namespace+'stru'):
        for element in stru_elem.find(namespace+'element'):
            for start in element.iter(namespace+'start'):
                toc["toc"].append({"nomenclature":stru_elem.find(namespace+'nomenclature').text,"start":start.get('sequence_number')})
    bookObj['toc'] = toc

    #cover image
    elem = root.find(namespace+'img')
    if elem.find(namespace+'sequence_number').text == "1":
        fileobj = elem.find(namespace+'file')
        bookObj["cover_img"] = fileobj.attrib[w3cns+'href']
    return bookObj

    def OL_upload():
        pass

    del OL_bulk_upload():
pass
