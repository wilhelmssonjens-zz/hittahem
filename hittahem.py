from bs4 import BeautifulSoup
import requests
import urllib3
#import dryscrape
import re


class Apartment(object):
    def __init__(self):
        f = open("example_split", 'r')
        soup = BeautifulSoup(f, 'html.parser')
        self.rent = Apartment.get_rent(soup)
        self.address = Apartment.get_address(soup)
        self.floor = Apartment.get_floor(soup)
        self.top_floor = Apartment.get_top_floor(soup)
        self.square_meters = Apartment.get_square_meters(soup)
        self.rooms = Apartment.get_rooms(soup)
        self.publish_day = Apartment.get_publish_day(soup)
        self.publish_month = Apartment.get_publish_month(soup)
        self.publish_year = Apartment.get_publish_year(soup)

    def get_rent(soup):
        rent = soup.find_all("p", 'rent')
        return int(re.findall("\d+\,\d+", rent[0].get_text())[0].replace(',', ''))

    def get_address(soup):
        address = soup.find_all("p", 'address')
        return address[0].get_text()

    def get_floor(soup):
        floor = soup.find_all('p', 'floor')
        return re.findall(r'\d+', floor[0].get_text())[0]

    def get_top_floor(soup):
        floor = soup.find_all('p', 'floor')
        return re.findall(r'\d+', floor[0].get_text())[1]

    def get_square_meters(soup):
        sq_m = soup.find_all('div', 'squaremeters')
        return float(re.findall("\d+\.\d+", sq_m[0].find_all('b')[0].get_text())[0])

    def get_rooms(soup):
        rooms = soup.find_all('div', 'squaremeters')
        return int(re.findall(r"\d+", rooms[0].find_all('p')[1].get_text())[0])

    def get_movein_day(soup):
        movein_day = soup.find_all('div', 'moveindate')
        return int(re.findall(r"\d+", movein_day[0].find_all('p', 'day')[0].get_text())[0])

    def get_movein_month(soup):
        movein_month = soup.find_all('div', 'moveindate')
        return month_to_num("".join(re.findall("[a-zA-Z]", movein_month[0].find_all('p', 'day')[0].get_text())))

    def get_movein_year(soup):
        movein_year = soup.find_all('div', 'moveindate')
        return int(movein_year[0].find_all('p', 'year')[0].get_text())

    def get_publish_day(soup):
        movein_day = soup.find_all('div', 'publishdate')
        return int(re.findall(r"\d+", movein_day[0].find_all('p', 'day')[0].get_text())[0])

    def get_publish_month(soup):
        movein_month = soup.find_all('div', 'publishdate')
        return month_to_num("".join(re.findall("[a-zA-Z]", movein_month[0].find_all('p', 'day')[0].get_text())))

    def get_publish_year(soup):
        movein_year = soup.find_all('div', 'publishdate')
        return int(movein_year[0].find_all('p', 'year')[0].get_text())


def month_to_num(month):
    calendar = {'januari': '01', 'Jan': '01', 'februari': '02', 'Feb': '02', 'mars': '03', 'Mar': '03',
                        'april': '04', 'Apr': '04', 'maj': '05', 'May': '05', 'juni': '06', 'Jun': '06', 'juli': '07',
                        'Jul': '07', 'augusti': '08', 'Aug': '08', 'september': '09', 'Sep': '09', 'oktober': '10',
                        'Oct': '10', 'november': '11', 'Nov': '11', 'december': '12', 'Dec': '12'}
    return calendar[month]


def read_boplats(boplats):
    # READ DATA GENERATED BY JAVA SCRIPT WITH DRYSCRAPE
    # Installation a bit hairy:
    # https://github.com/niklasb/dryscrape
    # Start dryscrape session
    
    print(boplats + num_hits_boplats)
    session = dryscrape.Session()
    session.visit(boplats)
    response = session.body()
    soup = BeautifulSoup(response, "html.parser")
    # "objectlist" hardcoded ID for the js-generated table containing data.
    boplats_data = soup.find(id="objectlist")
    #print(boplats_data)
    return boplats_data


def separate_boplats_data(boplats_data):
    #print(soup.prettify())
    entries_list = []
    for link in boplats_data.find_all(class_="item imageitem"):
        entries_list.append(link)
    return entries_list


def main():
    boplats = "https://nya.boplats.se/sok#itemtype=1hand"
    # boplats_data = read_boplats(boplats)
    # Tmp file read pga slow to get data from boplats everytime
    f = open('output_example.txt', "r")
    boplats_data = BeautifulSoup(f, "html.parser")
    aba = separate_boplats_data(boplats_data)
    print(aba[30])


if __name__ == '__main__':
    main()
