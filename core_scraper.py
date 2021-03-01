from bs4 import BeautifulSoup
import requests
import time 
TEST_URL = "https://sfbay.craigslist.org/search/sby/hhh?s=120&availabilityMode=0&excats=2-38-1-24-34-22-22-1&nh=109&nh=32&nh=34&nh=35&nh=41&nh=44"

class CoreScraper():
    def __init__(self, url_str = TEST_URL, debug = True):
        self.url = url_str 
        self.debug = debug

    def scrape_new_houses(self, saved_house_detail):
        cur_house_detail = self.scrape_housing()

        cur_house_keys = cur_house_detail.keys()        

        new_house_detail = {}
        for key in cur_house_keys:
            if key not in saved_house_detail:
                new_house_detail[key] = cur_house_detail[key]
        return new_house_detail


    def scrape_housing(self):
        if self.debug:
            print("Debug Scraper Running...")
            return self.debug_scraper()
        else: 
            return self.pro_scraper()
    
    def debug_scraper(self):
        html_file = open('craiglist.html', 'r')
        file = html_file.read()
        soup = BeautifulSoup(file, 'html.parser')
        next_button = soup.findAll("a", class_="button next")[0]
        next_button_link = next_button['href']
        house_listing = soup.findAll("div", class_="result-info")
        print("There are currently %d " % len(house_listing))

        house_listing_map= {} 
        for index, cur_house_listing in enumerate(house_listing): 
            print("House : %d of %d" %(index, len(house_listing)))
            house_data = {} 
            detail_page_soup = cur_house_listing.findAll("a", class_= "result-title hdrlnk")[0]
            time_info_soup = cur_house_listing.findAll("time")
            price_soup = cur_house_listing.findAll("span", class_= "result-price")[0]
            house_data["URL"] = detail_page_soup["href"]
            house_data["ID"] = detail_page_soup["id"].split("_")[1]
            house_data["TITLE"] = detail_page_soup.string
            house_data["PRETTY_DATE"] =  time_info_soup[0]["title"]
            house_data["POSTED_DATE"] = time_info_soup[0]["datetime"]
            house_data["PRICE"] = price_soup.string
            additional_details = self.scrape_house_detail(house_data["URL"])
            house_data.update(additional_details)
            house_listing_map[house_data["ID"]] = house_data
        return house_listing_map

    def pro_scraper(self, url):
        craiglist_site = requests.get(url)
        # html_file.write(craiglist_site.text)
        # print(craiglist_site.text)
        soup = BeautifulSoup(craiglist_site, 'html.parser')
        next_button = soup.findAll("a", class_="button next")[0]
        next_button_link = next_button['href']
        house_listing = soup.findAll("div", class_="result-info")
        house_listing_list = [] 
        for cur_house_listing in house_listing: 
                house_data = {} 
                detail_page_soup = cur_house_listing.findAll("a", class_= "result-title hdrlnk")[0]
                time_info_soup = cur_house_listing.findAll("time")
                price_soup = cur_house_listing.findAll("span", class_= "result-price")[0]
                house_data["URL"] = detail_page_soup["href"]
                house_data["ID"] = detail_page_soup["id"].split("_")[1]
                house_data["TITLE"] = detail_page_soup.string
                house_data["PRETTY_DATE"] =  time_info_soup[0]["title"]
                house_data["POSTED_DATE"] = time_info_soup[0]["datetime"]
                house_data["PRICE"] = price_soup.string
                additional_details = scrape_house_detail(house_data["URL"])
                house_data.update(additional_details)
                time.sleep(5) # Sleep for 5 second for safety 
        # If there is a link to the next page then use that link and continue with making the list
        additional_house_list = self.pro_scraper(self.url[:28] + next_button_link)
        house_listing_list.append(additional_house_list)
        return house_listing_list


    def scrape_house_detail(self, url: str):
        if self.debug:                                 
            detail_page = open("house_detail.html", "r")
            house_detail_soup = BeautifulSoup(detail_page.read(), "html.parser")
        else:
            detail_page = requests.get(url)        
            house_detail_soup = BeautifulSoup(detail_page.text, "html.parser")

            # house_detail_file = open("house_detail.html", "w")
            # house_detail_file.write(detail_page.text)
        
        house_data = {}

        map_detail_soup =  house_detail_soup.find("div", {"id": "map"})
        map_address_soup = house_detail_soup.find("div", {"class": "mapaddress"})
        house_data["LAT"] = map_detail_soup["data-longitude"]
        house_data["LONG"] = map_detail_soup["data-latitude"]
        house_data["ADDRESS"] = map_address_soup.string

        house_attrib_soup = house_detail_soup.findAll("p", class_ = "attrgroup")[1] 
        attrib_list =  house_attrib_soup.findAll("span")
        attrib_text = ""
        for attributes in attrib_list:
                attrib_text = attrib_text + attributes.string + " | "
        house_data["ATTRIBUTE"] = attrib_text
        house_text_soup = house_detail_soup.find("section", {"id": "postingbody"})
        house_text_tags = house_text_soup.findAll("li")
        detail_text = ""
        for house_detail_tag in house_text_tags: 
                detail_text = detail_text + house_detail_tag.string + "\n"
        house_data["DETAIL"] = detail_text
        return house_data

