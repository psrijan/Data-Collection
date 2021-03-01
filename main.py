from core_scraper import CoreScraper
from emailme import EmailDetails
import json 

class ScraperMain:
    def __init__(self):
        self.choices = {
            "1": "NEW_LISTING", 
            "2": "ALL_LISTING", 
        }
        self.email_enabled = True
        self.emailModule = EmailDetails()
        self.coreScraper = CoreScraper()
        self.file_name = "housedetail.json" 
        self.read_file()
    
    def read_file(self):
        try:
            with open(self.file_name, "r", encoding = "utf8") as open_file:
                self.saved_house_detail = json.load(open_file)        
        except FileNotFoundError:
            print("First Time Use... Creating new file %s" %(self.file_name))
            with open(self.file_name, "w", encoding = "utf8") as open_file:
                json.dump({}, open_file)
                self.saved_house_detail = json.load(open_file)
                print("Successfully Created New File")
        except EOFError:
            print("File must be empty: ")
            self.saved_house_detail = {}
            
    def print_options(self):
        print("1. See New Listing")
        print("2. List all suitable listing")
        choice = input("Enter your choice? ")

        cur_option = self.choices[choice]

        if cur_option == "NEW_LISTING":
            house_details = self.coreScraper.scrape_new_houses(self.saved_house_detail)
        elif cur_option == "ALL_LISTING":
            house_details = self.coreScraper.scrape_housing()
        final_house_str = self.format_house_details(house_details)            

        print("Total Number of Houses : %d" %(len(house_details.keys())))
        todays_picks = self.add_new_houses(house_details)
        self.emailModule.send_message(final_house_str)
        self.build_csv(todays_picks)
    
    def build_csv(self, todays_picks): 
        pass 

    def add_new_houses(self, house_details):
        todays_picks = {}
        for keys in house_details.keys():
            if not keys in self.saved_house_detail: 
                self.saved_house_detail[keys] = house_details[keys]            
                todays_picks[keys] = house_details[keys]
       
        with open(self.file_name , "w", encoding = "utf8") as file: 
            json.dump(house_details, file)
            print("Save To File Successful...")
        return todays_picks

    def format_house_details(self, house_details):
        final_str_template = """------ \n
        Title: %s
        Address: %s
        Price: %s 
        Url: %s
        ---------------\n
        """
        final_str =""
        i =0
        for key in house_details.keys():
            cur_house = house_details[key]
            cur_house_str = final_str_template  %(cur_house["TITLE"], cur_house["ADDRESS"], cur_house["PRICE"], cur_house["URL"])
            final_str += cur_house_str
            i += 1
            if i == 3:
                break
        print("Final String: %s " %final_str)
        email_message = """ Subject: Pick For The Day

        %s""" %final_str
        print("EMAIL MESSAGE")

        print(email_message)
        return self.safe_str(email_message)

    def safe_str(self, obj):
        try: 
            return str(obj)
        except UnicodeEncodeError:
            return obj.encode('ascii', 'ignore').decode('ascii')
        return ""

if __name__ == "__main__":
    main = ScraperMain()
    main.print_options()