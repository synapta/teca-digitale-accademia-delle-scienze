 # -*- coding: utf-8 -*-

from StringIO import StringIO
import csv 
import json
import requests

book_URL = "https://docs.google.com/spreadsheets/d/13u2k8_MVktUBamh-UZec3ylDnXQfQIp7HZT8AgB0MOU/export?format=csv&id=13u2k8_MVktUBamh-UZec3ylDnXQfQIp7HZT8AgB0MOU&gid=715455760"
file_path = '/root/public/data/book.json'

with open(file_path, 'r' ) as old_file:
    old_list = json.load(old_file)


new_file_content = []
r = requests.get(book_URL)
if r.status_code != '200':
    new_content = r.text.encode('utf-8')
    f = new_content.splitlines()

    reader = csv.DictReader(f) 

    for line in reader:
        new_file_content.append(line)

    if len(new_file_content) >= len(old_list):
        with open(file_path, 'w') as outfile:
            json.dump(new_file_content, outfile, indent=4, ensure_ascii=False)
        print("New index written.")

else:
    print("Failed new index fetch")
