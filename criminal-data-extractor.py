import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import pandas as pd

criminal_ids = pd.read_csv("criminals.csv")

wanted_url = "https://www.interpol.int/notice/search/wanted/"

columns = ["criminal_id","present_family_name","forename","sex","dob","place_of_birth","language","nationality","height","weight","hair","eyes","charges"]
details = ["Criminal ID:","Present family name:","Forename:","Sex:","Date of birth:","Place of birth:","Language spoken:","Nationality:","Height:","Weight:","Colour of hair:","Colour of eyes:","Charges:"]

df = pd.DataFrame(columns=columns)

def getAvailCols(availables):
    avail_cols = []
    details = ["Criminal ID:","Present family name:","Forename:","Sex:","Date of birth:","Place of birth:","Language spoken:","Nationality:","Height:","Weight:","Colour of hair:","Colour of eyes:","Charges:"]
#     print("\nAvailables: ",availables)
    for available in availables:
#         print("\nAvailable: ",available)
        if(available.text == '\xa0'):
            continue
        elif(available.text in details):
            avail_cols.append(columns[details.index(available.text)])
#         print(avail_cols)
    return avail_cols

for criminal_id in criminal_ids.criminal_id:
#     print(criminal_id)
    url = wanted_url+str(criminal_id)
    response = requests.get(url)
    soup = bs(response.content,'lxml')
    availables = soup.findAll("td", {"class": "col1"})
    values = soup.findAll("td", {"class": "col2"})
#     if(not getAvailCols(availables)):
#         continue
    avail_cols = ["criminal_id","wanted_by"]
    avail_cols+=getAvailCols(availables)
    values_text = []
    values_text.append(criminal_id)
    values_text.append(soup.findAll("span", {"class": "nom_fugitif_wanted_small"})[0].text.split("authorities of")[-1].strip())
    for i,available in enumerate(availables):
        if(availables[i].text in details):
            value = values[i].text.replace('\t','').replace('\n','')
            values_text.append(value)
    values = []
    values.append(values_text)
    df_criminal = pd.DataFrame(values, columns=avail_cols)
    df = pd.concat([df,df_criminal], axis=0, ignore_index=True)
#     print(availables)
#     print(values)
dobs = []
for dob in df.dob:
    dob = str(dob).split(" ")[0]
    dobs.append(dob)
df.dob = dobs

df.to_csv("criminal_data.csv")