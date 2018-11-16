from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == "__main__":
    html = urlopen("http://www.google.ca")
    #print(html.read())
    soup = BeautifulSoup(html.read(), "html.parser")
    print(soup.prettify())
