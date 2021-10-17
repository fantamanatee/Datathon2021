import requests
from bs4 import BeautifulSoup
import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from collections import OrderedDict
import csv
import random

def estProfit(name_cont, soup):
    h3 = name_cont.find("h3")
    extension = h3.find('a')['href']
    URL2 = 'https://www.salvagebid.com' + extension
    # Instantiate an Options object
    # and add the "--headless" argument
    PATH2 = "C:\Program Files (x86)\chromedriver.exe"
    options2 = webdriver.ChromeOptions()
    options2.add_argument("headless")
    driver2 = webdriver.Chrome(PATH2, chrome_options=options2)
    driver2.get(URL2)

    time.sleep(5)
    # print(URL2,"      EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

    soup_file2=driver2.page_source
    soup2 = BeautifulSoup(soup_file2)
    sale_info = soup2.find('div',class_='lot-block sale-info')
    # print(sale_info.prettify())
    ul = sale_info.find_all('li', class_='lot-block-list-item')
    x = 0
    for li in ul:
        print(x)
        x+=1
        print(li.prettify())
        print("---")
    cash_val_cont = ul[5]
    cash_val_cont2 = ul[6]
    # print(cash_val_cont)
    cash_val_str = cash_val_cont.find('span').text.replace(',','')
    cash_val_str2 = cash_val_cont2.find('span').text.replace(',','')
    if(cash_val_str.isnumeric()):
        # print(cash_val_str)
        cash_val = int((cash_val_str[1:-3]))
    elif(cash_val_str.isnumeric()):
        cash_val = int((cash_val_str2[1:-3]))
    else:
        cash_val=0

    est_repair_cont = ul[6]
    est_repair_cont2 = None
    try:
        est_repair_cont2 = ul[7]
    except(IndexError):
        est_repair_cont2 = est_repair_cont
    est_repair_str = est_repair_cont.find('span').text.replace(',','')
    est_repair_str2 = est_repair_cont2.find('span').text.replace(',','')
    if(est_repair_str.isnumeric()):
        est_repair_val = int(est_repair_str[1:-3])
    elif(est_repair_str2.isnumeric()):
        est_repair_val = int(est_repair_str2[1:-3])
    else:
        est_repair_val = 0
    print(est_repair_val)

    if(est_repair_val==0):
        if(not cash_val == 0):
            est_repair_val = random.randint(cash_val-3000, cash_val+3000)
        else:
            cash_val = random.randint(10000,30000)
            est_repair_val = random.randint(cash_val-3000, cash_val+3000)
    driver2.close()
    return cash_val - est_repair_val


numData = "100"#input("Enter how many cars to collect data of: ")
URL = "https://www.salvagebid.com/salvage-cars-for-sale?page=6&per_page="+numData+"&type=car"
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
item_id = 200
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
    name_parts = (h3.find("a").text).split()
    year = name_parts[0]
    make = name_parts[1]
    model = name_parts[2]

    #names assigned properly
    #to-do: split into year, make, model

    the_small_dict['Year'] = year
    the_small_dict['Make'] = make
    the_small_dict['Model'] = model

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
    title = title.lower()
    if('clea' in title and not title== None):
        title = 'Clean'
    elif('salv' in title and not title== None):
        title = 'Salvage'
    elif('repo' in title and not title==None):
        title = 'Reposession'
    else:
        title = 'Other'
    the_small_dict['Title'] = title

    the_small_dict['Est. Profit'] = random.randint(-5000,5000)#estProfit(name_cont, soup)
    #TODO: reduce titles to salvage, clean, or none

    # location_cont = rest_cont.find('li', class_ = 'location')
    # location = location_cont.find('span')['location']
    # the_small_dict['Loc'] = location[-2:] WONT WORK IDKKKKKKKK

    the_big_dict[item_id] = the_small_dict


#adding manual damage assessment
# worth = input('Enter your opinion on the car\'s worth, based on damage assessment (separated by spaces) (out of 10): ').split()
# for w in range(len(the_big_dict)):
#     # if(w<len(worth)):
#     #     toAppend = round(float(worth[w]),1)
#     # else:
#     #     toAppend = round(random.random()*10,1)
#     toAppend = round(random.randint(1000,10000),0)
#     the_big_dict[w+1]['Worth'] = toAppend
#2.5 1.6 4.6 6.0 4.0 2.0 6.0 3.0 3.0 5.4 

#sorting each sub_dict by key
for key in the_big_dict:
    the_big_dict[key] = OrderedDict(sorted(the_big_dict[key].items()))

pprint.pprint(the_big_dict)

header = ['ID','Year', "Make", "Model", 'Odometer', 'Title','Damage', 'Engine','Est. Profit']

toWrite = []

for x in range(201,301):
    toAppend = [x]
    currDict = the_big_dict[x]

    toAppend.append(currDict['Year'])
    toAppend.append(currDict['Make'])
    toAppend.append(currDict['Model'])
    toAppend.append(currDict['Odometer'])
    toAppend.append(currDict['Title'])
    toAppend.append(currDict['Damage'])
    toAppend.append(currDict['Engine'])
    toAppend.append(currDict['Est. Profit'])

    toWrite.append(toAppend)

with open('damaged_car_data.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # writer.writerow(header)
    writer.writerows(toWrite)


# print(result_containers[0].prettify())