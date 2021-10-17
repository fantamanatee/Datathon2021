import requests
from bs4 import BeautifulSoup

numData = input("Enter how many cars to collect data of: ")
URL = "https://www.salvagebid.com/salvage-cars-for-sale?per_page="+numData+"&type=car"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

body = soup.find(id="spa-react-root")
page_content = body.find_all("div", class_="page-content")


print(page_content)