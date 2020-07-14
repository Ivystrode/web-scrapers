#https://www.onthemarket.com/for-sale/property/plymouth/

import requests 
from bs4 import BeautifulSoup 
import pandas 
import re 
import numpy as np
from datetime import datetime

import storage

print("\nProperty data scraper. UK cities only.\n")
search_time = datetime.now().strftime("%Y-%m-%d_%H%M")

city = input("Enter city name: ")
radius = input("Enter geographic search radius (maximum 40): ")

accepted_radii = [1, 3, 5, 10, 15, 20, 30, 40]

if int(radius) not in accepted_radii:
    print("Radius must be 40 or less")
    print("Enter one of the following: 1, 3, 5, 10, 15, 20, 30, 40")
    radius = input("Re-enter search radius: ") 

headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

r = requests.get(f"https://www.onthemarket.com/for-sale/property/{city}/?radius={radius}", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
soup = BeautifulSoup(c, "html.parser")
all = soup.find_all("li", {"class":"result property-result panel new first"})


for page in soup.find_all("ul", {"class":"pagination-tabs"}):
    for num in soup.find_all("li")[-2]:
            numpages = page.find_all("a",{"class":""})[-1].text

print(str(numpages) + " pages of results...\n")


if len(all) < 1:
    print("\nNothing found. Ensure city name entered correctly.")

#https://www.onthemarket.com/for-sale/property/plymouth/?page=0&radius=5.0
i = 0
proplist = []
#base_url=(f"https://www.onthemarket.com/for-sale/property/{city}/?page={page}&?radius={radius}", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
chars="qwertyuiopasdfghjklzxcvbnm,"

if int(numpages) > 50:
    cont = input("Over 50 pages of results. Are you sure you wish to continue? y/n\n")
    if "y" in cont:
        pass
    else:
        print("Program terminated")
        exit()

for page in range(0, int(numpages)+1, 1):
    r = requests.get(f"https://www.onthemarket.com/for-sale/property/{city}/?page=" + str(page) + "&?radius={radius}", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup=BeautifulSoup(c, "html.parser")
    all = soup.find_all("li", {"class":"result"})

    for item in all:
        property = {}
        i += 1

        try:
            print(str(item.find("span", {"class":"title"}).text))
        except:
            print("Unknown number of bedrooms")

        try:
            property["Price"]=item.find("a", {"class":"price"}).text
            property["Price"] = ''.join(filter(str.isdigit, property["Price"]))
            if property["Price"] == "":
                property["Price"] = "0"
        except:
            property["Price"] = "0"

        property["Address"]=item.find_all("span", {"class":"address"})[0].text
        try:
            property["Beds"]=item.find("span", {"class":"title"}).text
            property["Beds"]= ''.join(filter(str.isdigit, property["Beds"]))
        except:
            property["Beds"]="0"
        try:
            property["Agent_Name"]=item.find("a", {"class":"marketed-by-link"}).text
        except:
            property["Agent_Name"]="None"
        try:
            property["Agent_tel"]=item.find("span", {"class":"call"}).text #find("span").text
        except:
            property["Agent_tel"]="None"
        property["Website"] = "OTM"
        property["Acquire_time"] = str(search_time)
        proplist.append(property)

if len(proplist) > 0:
    print (str(len(proplist)) + " properties found")
    print ("On " + str(numpages) + " pages\n")
    df = pandas.DataFrame(proplist)

    try:
        avprice = np.asarray(df["Price"], dtype=np.int).mean()
        print("Average Price: ")
        print(avprice)
        print("Properties with price not explicitly specified excluded from average")

        with open("average_prices.txt", 'a') as file:
            file.write(f"\n{search_time}_Average Price from OTM for properties within {radius} miles of {city}: " + "£" + str(int(avprice)))
    
    except:
        print("Cannot calculate average")

    save_prompt = input("\nSave results as spreadsheet? y/n: ")

    if "y" in save_prompt:
        filename = f"{search_time}_{city}"
        df.to_csv(f"{filename}.csv")
        print(f"Saved data in file: '{filename}.csv'")
    else:
        print("No spreadsheet saved")

    print(f"Saving {len(proplist)} properties to {city.upper()} database...")
    storage.connect(city)

    properties_saved = 0
    properties_existing = 0

    for p in proplist: # consider adding tqdm - and removing print statements in storage
        if storage.insert(city, 'N/A', p['Price'], p['Address'], p['Beds'], 'N/A', 'N/A', p['Agent_Name'], p['Agent_tel'], p['Website'], p['Acquire_time']) == 'new':
            properties_saved += 1
        else:
            properties_existing += 1
        print(f"Saved {properties_saved} to {city} - {properties_existing} already in database")

    print("Saved to DB")