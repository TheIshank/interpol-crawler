import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import pandas as pd

# Function to identify which columns are available for the given crimminal profile


def getAvailCols(availables):
    avail_cols = []
    avail_cols.append("criminal_id")
    details = ["Criminal ID:", "Present family name:", "Forename:", "Sex:", "Date of birth:", "Place of birth:",
               "Language spoken:", "Nationality:", "Height:", "Weight:", "Colour of hair:", "Colour of eyes:", "Charges:"]
    for available in availables:
        if(available.text == '\xa0'):
            continue
        elif(available.text in details):
            avail_cols.append(columns[details.index(available.text)])
    return avail_cols


criminal_ids = pd.read_csv("criminals.csv")
wanted_url = "https://www.interpol.int/notice/search/wanted/"
columns = ["criminal_id", "present_family_name", "forename", "sex", "dob", "place_of_birth",
           "language", "nationality", "height", "weight", "hair", "eyes", "charges"]
details = ["Criminal ID:", "Present family name:", "Forename:", "Sex:", "Date of birth:", "Place of birth:",
           "Language spoken:", "Nationality:", "Height:", "Weight:", "Colour of hair:", "Colour of eyes:", "Charges:"]
df = pd.DataFrame(columns=columns)

for criminal_id in criminal_ids.criminal_id[1112:]:
    print(criminal_id)
    url = wanted_url+str(criminal_id)
    response = requests.get(url)
    soup = bs(response.content, 'lxml')
    availables = soup.findAll("td", {"class": "col1"})
    values = soup.findAll("td", {"class": "col2"})
    avail_cols = getAvailCols(availables)
    values_text = []
    values_text.append(criminal_id)
    for i, available in enumerate(availables):
        if(availables[i].text in details):
            value = values[i].text.replace('\t', '').replace('\n', '')
            values_text.append(value)
    values = []
    values.append(values_text)
    df_criminal = pd.DataFrame(values, columns=avail_cols)
    df = pd.concat([df, df_criminal], axis=0, ignore_index=True)

df.to_csv("criminal_data.csv")
