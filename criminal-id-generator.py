import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# Function to generate possile urls. You can generate more urls by uncommenting the commented region and commenting line 37


def generate_urls(url):
    countries = pd.read_csv("countries.csv", header=None, delimiter=";")
    hair = pd.read_csv("hair.csv", header=None, delimiter=";")
    eyes = pd.read_csv("eyes.csv", header=None, delimiter=";")
    age = range(0, 101)
    filters = {}
    filters["Sex"] = [" ", "M", "F", "U"]
    filters["Nationality"] = [" "]+list(countries[0])
    filters["Hair"] = [" "]+list(hair[0])
    filters["Eyes"] = [" "]+list(eyes[0])
    filters["RequestingCountry"] = [" "]+list(countries[0])
    filters["current_age_mini"] = age
    filters["current_age_maxi"] = age
    links = pd.DataFrame(columns=["urls"])
    urls = [url]
    temp_url1 = url+"/(search)/1"
    for sex in filters["Sex"]:
        if(sex != " "):
            temp_url2 = temp_url1+"/(Sex)/"+sex
        else:
            temp_url2 = temp_url1
        for nationality in filters["Nationality"]:
            if(nationality != " "):
                temp_url3 = temp_url2+"/(Nationality)/"+str(nationality)
            else:
                temp_url3 = temp_url2
            for max_age in [" ", 100, 120]:
                if(max_age != " "):
                    temp_url4 = temp_url3+"/(current_maxi_age)/"+str(max_age)
                else:
                    temp_url4 = temp_url3
                urls.append(temp_url4)
#             for hair in filters["Hair"]:
#                 if(hair!=" "):
#                     temp_url5 = temp_url4+"/(Hair)/"+hair
#                 else:
#                     temp_url5 = temp_url4
#                 for eyes in filters["Eyes"]:
#                     if(eyes!=" "):
#                         temp_url6 = temp_url5+"/(Eyes)/"+eyes
#                     else:
#                         temp_url6 = temp_url5
#                     for req_country in filters["RequestingCountry"]:
#                         if(req_country!=" "):
#                             temp_url7 = temp_url6+"/(RequestingCountry)/"+str(req_country)
#                         else:
#                             temp_url7 = temp_url6
#                     urls.append(temp_url7)
    links["urls"] = urls
    links.to_csv("urls.csv")

# Function to iterate through all pages for a given url and criminal count and fetch criminal ids


def find_more_criminals(url, no_of_criminals):
    criminal_ids = set()
    for offset in range(9, no_of_criminals+1, 9):
        offset_url = url+"/(offset)/"+str(offset)
        response = requests.get(offset_url)
        soup = bs(response.content, 'lxml')
        links = soup.findAll("a", {"class": "details"})
        for link in links:
            criminal_ids.add(link['href'].split('/')[-1])
    return criminal_ids

# Function to fetch criminal ids from a given url


def number_of_criminals(url):
    response = requests.get(url)
    soup = bs(response.content, 'lxml')
    page_counter = soup.findAll("span", {"class": "orange"})
    return int(page_counter[0].contents[0].replace("Search result : ", ""))

# Function to find all criminal ids for a given url and all its pages


def add_to_criminals(url):
    criminal_ids = set()
    no_of_criminals = number_of_criminals(url)
    if(no_of_criminals < 1):
        return criminal_ids
    response = requests.get(url)
    soup = bs(response.content, 'lxml')
    links = soup.findAll("a", {"class": "details"})
    for link in links:
        criminal_ids.add(link['href'].split('/')[-1])
    if(no_of_criminals > 9):
        criminal_ids = criminal_ids.union(
            find_more_criminals(url, no_of_criminals))
    return criminal_ids


# URLs written to urls.csv
generate_urls("https://www.interpol.int/notice/search/wanted")

crime_data = pd.DataFrame(columns=["criminal_id"])
urls = pd.read_csv("urls.csv")
criminal_ids = set()

# Criminal ids fetched for each url and written to criminals.csv
for url in urls['urls']:
    print(url)
    criminal_ids = criminal_ids.union(add_to_criminals(url))

crime_data['criminal_id'] = list(criminal_ids)
crime_data.to_csv("criminals.csv", index=False)
