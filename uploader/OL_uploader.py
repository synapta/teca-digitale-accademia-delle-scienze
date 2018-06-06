import pandas as pd
import json
import ast
import re

bookdf = pd.read_csv('book.csv', dtype=str, encoding='utf-8')
bookdf = bookdf.fillna(value="nan")

for index,row in bookdf.iterrows():
    print("Book",index)

    creator = re.sub(r"<.*>", "", row['creator'])
    year = row['date']
    id = row['identifier']
    publisher = row['publisher']
    publisher = re.sub(r",\s1[0-9]{3}", "", row['publisher'])
    publisher = re.sub(r"\[1[0-9]{3}\]", "", publisher)
    publisher = re.sub(r"\-1[0-9]{3}", "", publisher)
    publisher = re.sub(r"[0-9\,\-\[]*$", "", publisher)
    publisher = re.sub(r", ]$", "", publisher)
    title = row['title']
    toc = row['toc']

    if re.search(r"1[0-9]{3}", year) == None:
        year = ""

    if len(publisher) != 0 and publisher != "nan":
        if publisher[-1]==",":
            publisher = publisher[0:-1]
    else:
        #empty or nan publisher
        publisher=""

    OL_toc = ""
    if toc != "[]":
        for elem in toc[2:-2].split("\", \""):
            number = re.search(r"([0-9])+", elem).group(0)
            elem = elem.replace(" "+number, "")
            elem = re.sub(r"[\[\]]", "", elem)
            if OL_toc == "":
                OL_toc = "* | "+elem+" | "+number+"\n"
            else:
                OL_toc = OL_toc+"* | "+elem+" | "+number+"\n"

    with open("OL.csv", "a") as f:
        f.write(str(index)+","+row['lotto']+","+id+",https://archive.org/stream/"+id+",\""+title+"\",\""+creator+"\",\""+publisher+"\","+year+",\""+str(OL_toc)+"\"\n")
