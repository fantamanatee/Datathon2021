import requests
from bs4 import BeautifulSoup
import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from collections import OrderedDict
import csv

numData = "10"#input("Enter how many cars to collect data of: ")
URL = "https://www.salvagebid.com/salvage-cars-for-sale?per_page="+numData+"&type=car"
# Instantiate an Options object
# and add the "--headless" argument
PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, chrome_options=options)
driver.get(URL)

time.sleep(5)

soup_file=driver.page_source
soup = BeautifulSoup(soup_file)
# body = soup.find('body')
spa_react_root = soup.find(id="spa-react-root")
# page_content = spa_react_root.find("div", class_="page-content")
# # container = page_content.find("div",class_='container')
# vehicle_content = page_content.find("div",class_ = "vehicle-content")
result_containers = spa_react_root.find_all("div",class_ = "result-item-data")
names_containers = spa_react_root.find_all("div",class_ = "result-item-name")
names = []
item_id = 0
the_big_dict = {#{0:{
    # 'year' = 2011,
    # 'model' = 'FORD',
    # 'make' = 'EDGE',
    # 'odometer' = 3232,
    # 'damage' = 'FLOOD',
    # 'start_code' = 'stationary',
    # 'title_type' = 'Salvage'
    # 'Location' = 'NJ'
}#}

for rest_cont in result_containers:
    item_id+=1
    the_small_dict = {}

    attribute_contents = rest_cont.find_all('span',class_='text-uppercase')

    name_cont = rest_cont.find('div',class_='result-item-name')
    h3 = name_cont.find("h3")
    name = h3.find("a").text
    names.append(name)
    #names assigned properly
    #to-do: split into year, make, model

    the_small_dict['Year'] = name
    the_small_dict['Make'] = name
    the_small_dict['Model'] = name

    odometer_str = (attribute_contents[0]['title'])
    odometer = int(odometer_str[:-2])
    the_small_dict['Odometer'] = odometer
    #odometer works

    damage = attribute_contents[1]['title']
    the_small_dict['Damage'] = damage

    engine_cont = rest_cont.find('li', class_ = 'engine')
    engine = engine_cont.find('span')['title']
    the_small_dict['Engine'] = engine

    #TODO: reduce titles to salvage, clean, or none
    title_cont = rest_cont.find('li', class_ = 'title')
    title = title_cont.find('span')['title']
    the_small_dict['Title'] = title
    #TODO: reduce titles to salvage, clean, or none

    # location_cont = rest_cont.find('li', class_ = 'location')
    # location = location_cont.find('span')['location']
    # the_small_dict['Loc'] = location[-2:] WONT WORK IDKKKKKKKK

    the_big_dict[item_id] = the_small_dict


#adding manual damage assessment
worth = input('Enter your opinion on the car\'s worth, based on damage assessment (separated by spaces) (out of 10): ').split()
for w in range(len(the_big_dict)):
    if(w<len(worth)):
        toAppend = round(float(worth[w]),1)
    else:
        toAppend = 0.0
    the_big_dict[w+1]['Worth'] = toAppend
#2.5 1.6 4.6 6.0 4.0 2.0 6.0 3.0 3.0 5.4 

#sorting each sub_dict by key
for key in the_big_dict:
    the_big_dict[key] = OrderedDict(sorted(the_big_dict[key].items()))

pprint.pprint(the_big_dict)

header = ['ID','Year', "Make", "Model", 'Odometer', 'Title','Damage', 'Engine','Worth']

toWrite = []

for x in range(1,len(the_big_dict)+1):
    toAppend = [x]
    currDict = the_big_dict[x]

    toAppend.append(currDict['Year'])
    toAppend.append(currDict['Make'])
    toAppend.append(currDict['Model'])
    toAppend.append(currDict['Odometer'])
    toAppend.append(currDict['Title'])
    toAppend.append(currDict['Damage'])
    toAppend.append(currDict['Engine'])
    toAppend.append(currDict['Worth'])

    toWrite.append(toAppend)

with open('damaged_car_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(toWrite)


# print(result_containers[0].prettify())