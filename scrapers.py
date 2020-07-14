from bs4 import BeautifulSoup as bs

class Scraper(self, search_url, base_url, result_tag, results_pages, num_pages):

    accepted_radii = [1, 3, 5, 10, 15, 20, 30, 40]
    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    def __init__(self, self.search_url, self.base_url, self.result_tag, self.results_pages, self.num_pages):
        self.search_url = search_url
        self.base_url = base_url
        self.result_tag = result_tag
        self.results_pages = results_pages
        self.num_pages = num_pages

    def save(city, proplist):    
        print(f"Saving {len(proplist)} properties to {city.upper()} database...")
        storage.connect(city)

        properties_saved = 0
        properties_existing = 0

        for p in proplist:
            if storage.insert(city, p['Date_Listed'], p['Price'], p['Address'], p['Beds'], p['Bathrooms'], p['Reception_rooms'], p['Agent_Name'], p['Agent_tel'], p['Website'], p['Acquire_time']) == 'new':
                properties_saved += 1
            else:
                properties_existing += 1
            print(f"Saved {properties_saved} to {city} - {properties_existing} already in database")

        print("Saved to DB")


    def scan():
        if radius not in accepted_radii:
            print("Radius must be 40 or less")
            print("Enter one of the following: 1, 3, 5, 10, 15, 20, 30, 40")
            exit()
        
        r = requests.get(self.search_url)
        c = r.content
        s = bs(c, "html.parser")
        all = s.find_all(self.result_tag)

        for page in self.results_pages:
            print(str(self.numpages) + " pages of results...\n")

        if len(all) < 1:
            print("\nNothing found. Ensure city name entered correctly.")

        i = 0
        proplist = []
        chars="qwertyuiopasdfghjklzxcvbnm,"

        if int(numpages) > 50:
            cont = input("Over 50 pages of results. Are you sure you wish to continue? y/n: ")
            if "y" in cont:
                pass
            else:
                print("Program terminated")
                exit()
                
        print("\nScanning " + str(self.num_pages) + " pages...\n")

        for page in tqdm(range(1, int(self.num_pages)=1, 1)):
            r = requests.get(self.base_url + str(page))
            c = r.content
            s=BeautifulSoup(c, "lxml")
            all = s.find_all(self.result_tag)

                for item in all:

                    property = {}
                    i += 1

                    property["Date_Listed"]=item.find("p", {"class":"top-half listing-results-marketed"}).find("small").text.replace(" ", "").replace("\n", "").replace("Listedon", "").replace("by", "")
                    try:
                        property["Price"] = item.find("a", {"class":"listing-results-price text-price"}).text.replace("\n", "").replace("Offersinregionof", "").replace(" ", "").replace("Offersover", "")
                        property["Price"] = ''.join(filter(str.isdigit, property["Price"]))
                        if property["Price"] == "":
                            property["Price"] = "0"
                    except:
                        property["Price"] = "0"

                    property["Address"]=item.find_all("a", {"class":"listing-results-address"})[0].text

                    try:
                        property["Beds"]=item.find("span", {"class":"num-icon num-beds"}).text
                    except:
                        property["Beds"]="0"
                    try:
                        property["Bathrooms"]=item.find("span", {"class":"num-icon num-baths"}).text
                    except:
                        property["Bathrooms"]="0"
                    try:
                        property["Reception_rooms"]=item.find("span", {"class":"num-icon num-reception"}).text
                    except:
                        property["Reception_rooms"]="0"
                    try:
                        property["Agent_Name"]=item.find("p", {"class":"top-half listing-results-marketed"}).find("span").text
                    except:
                        property["Agent_Name"]="None"
                    try:
                        property["Agent_tel"]=item.find("span", {"class":"agent_phone"}).find("span").text
                    except:
                        property["Agent_tel"]="None"
                    property["Website"] = "Zoopla"
                    property["Acquire_time"] = str(search_time)

                    proplist.append(property)


        
        

