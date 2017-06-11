from bs4 import BeautifulSoup
import requests
import urllib3
import re


class Apartment(object):
    def __init__(self, object_url):
        page = requests.get(object_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        specs = Apartment.get_apartment_attributes(soup)
        self.rooms = specs[0][0]
        self.square_m = specs[0][1]
        self.rent = specs[1][0]+specs[1][1]
        # self.rent = specs[1][1]
        # self.occupancy_day = specs[2][1]
        # self.stairs = specs[3][1]
        # self.deadline = specs[4][1]

    def get_apartment_attributes(soup):
        main_content = soup.find(id="maincontent")
        table = main_content.find(text="Antal rum:").find_parent("table")
        specs = list()
        specs_num = list()
        for row in table.find_all("tr")[0:]:
            specs = ([cell.get_text(strip=False) for cell in row.find_all("td")])
            print(specs)
            specs_num.append(re.findall(r"[-+]?\d*\.\d+|\d+", specs[1]))
        print(specs_num)
        return specs_num

def month_to_num(month):
    calendar = {'januari': '01', 'februari': '02', 'mars': '03', 'april': '04', 'maj': '05', 'juni': '06', 'juli': '07',
                'augusti': '08', 'september': '09', 'oktober': '10', 'november': '11', 'december': '12'}
    return calendar[month]


def main():
    boplats = "https://nya.boplats.se/objekt/1hand/593A73FBFEF3179E0003B4F7"
    jens = Apartment(boplats)
    print(jens.rooms)
    print(jens.rent)
    print(jens.square_m)


if __name__ == '__main__':
    main()
