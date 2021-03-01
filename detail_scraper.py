import requests 
from bs4 import BeautifulSoup

def scrape_house_detail(url: str):
        # detail_page = requests.get(url)        
        # house_detail_soup = BeautifulSoup(detail_page.text, "html.parser")

        # house_detail_file = open("house_detail.html", "w")
        # house_detail_file.write(detail_page.text)
        house_data = {}

        detail_page = open("house_detail.html", "r")
        house_detail_soup = BeautifulSoup(detail_page.read(), "html.parser")

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

        print(house_data)
        return house_data

scrape_house_detail("hello")


