from bs4 import BeautifulSoup
import requests
import urllib3


def main():
    boplats = "https://nya.boplats.se/sok#&skip=30"
    page = requests.get(boplats)
    soup = BeautifulSoup(page.text, "lxml")
    print(soup.contents)

if __name__ == '__main__':
    main()