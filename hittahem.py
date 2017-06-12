from bs4 import BeautifulSoup
from geopy.geocoders import GoogleV3
import requests
import urllib3

import time
import gmplot
#import dryscrape
import re


class Apartment(object):
    def __init__(self, soup, geolocator):
        # f = open("example_split", 'r')
        # f = object
        # soup = BeautifulSoup(f, 'html.parser')
        self.rent = Apartment.get_rent(soup)
        self.area = Apartment.get_area(soup)
        self.address = Apartment.get_address(soup)
        self.location = Apartment.get_location(soup, geolocator)
        try:
            self.floor = Apartment.get_floor(soup)
        except:
            self.floor = -1
        try:
            self.top_floor = Apartment.get_top_floor(soup)
        except:
            self.top_floor = -1
        self.square_meters = Apartment.get_square_meters(soup)
        self.rooms = Apartment.get_rooms(soup)
        self.publish_day = Apartment.get_publish_day(soup)
        self.publish_month = Apartment.get_publish_month(soup)
        self.publish_year = Apartment.get_publish_year(soup)

    def get_rent(soup):
        rent = soup.find_all("p", 'rent')
        return int(re.findall("\d+\,\d+", rent[0].get_text())[0].replace(',', ''))

    def get_area(soup):
        address = soup.find_all("p", 'area')
        return address[0].get_text()

    def get_address(soup):
        address = soup.find_all("p", 'address')
        return address[0].get_text()

    def get_location(soup, geolocator):
        address = soup.find_all("p", 'address')
        tmpstring = address[0].get_text() + " Göteborg"
        location = geolocator.geocode(tmpstring)
        return location

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
    # print(boplats_data)
    return boplats_data


def separate_boplats_data(boplats_data):
    # print(soup.prettify())
    entries_list = []
    for link in boplats_data.find_all(class_="item imageitem"):
        entries_list.append(link)
    return entries_list

def get_apartment_list(apartment_datalist):
    # takes the list of <tr>...</tr> data-elements and creates apartmentobjects
    apartment_list = []
    for apartment_data in apartment_datalist:
        try:
            apartment_list.append(Apartment(apartment_data))
        except:
            print("Fel på apartment_data-element")

    return apartment_list

def get_apartment_list(apartment_datalist, geolocator):
    # takes the list of <tr>...</tr> data-elements and creates apartmentobjects
    apartment_list = []
    i = 0
    for apartment_data in apartment_datalist:
        #print(i)
        #if i > 2:
        try:
            tmpapartment = Apartment(apartment_data, geolocator)
            print("longitude = " + str(tmpapartment.location.longitude) + ". latitude = " + str(tmpapartment.location.latitude))
            apartment_list.append(tmpapartment)
            time.sleep(0.3)
            print(i)
        except:
            print("Fel på apartment_data-element, index i = " + str(i))
        i = i + 1
    return apartment_list

def get_longitudes(apartment_list):
    list = []
    for apartment in apartment_list:
        list.append(zip("adam", apartment.location.latitude))

    return list


def get_latitudes(apartment_list):
    list = []
    for apartment in apartment_list:
        list.append(zip("eva", apartment.location.longitude))

    return list

def main():
    boplats = "https://nya.boplats.se/sok#itemtype=1hand"
    # boplats_data = read_boplats(boplats)
    # Tmp file read pga slow to get data from boplats everytime
    f = open('output_example.txt', "r")
    boplats_data = BeautifulSoup(f, "html.parser")
    aba = separate_boplats_data(boplats_data)
    geolocator = GoogleV3()
    apartment_list = get_apartment_list(aba, geolocator)
    print(apartment_list[3].location.longitude)

    gmap = gmplot.GoogleMapPlotter(57.7, 11.9, 16)

    y = ['item1', 'item2']  # list of strings
    xdata = [57.7, 11.9] # list of numbers
    ADAM = list(zip(xdata))


    gmap.scatter(ADAM[0], ADAM[1],'k', size=40, marker=True)
    #lats = get_latitudes(apartment_list)
    #longs = get_longitudes(apartment_list)
    #print(longs[0])
    #gmap.plot(lats, longs, 'cornflowerblue', edge_width=10)
    #gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
    #gmap.scatter(lats, longs, 'k', marker=True)

    gmap.heatmap(ADAM[0], ADAM[1])

    gmap.draw("mymap.html")
if( __name__ == '__main__'):
    main()
