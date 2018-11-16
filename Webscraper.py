from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup

def get_file_name(file_string):
    return file_string[file_string.rfind("/")+1:]

def download_pdf(url):
    try:
        pdf_file = urlopen(url)
        name = get_file_name(url)
        print(name)
        file = open(name, "wb")
        file.write(pdf_file.read())
        file.close()
    except urllib.error.HTTPError:
        name = get_file_name(url)
        errmsg = " could not be found."
        print(name + errmsg)

if __name__ == "__main__":
    html = urlopen("http://www.gov.yk.ca/forms/all.html")
    #print(html.read())
    soup = BeautifulSoup(html.read(), "html.parser")
    #print(soup.prettify())
    pdflist = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href[-4:] == ".pdf":
            #parent = link.find_parent("p")
            #print(parent.get_text())
            pdflist.append(href.strip())
            #print(link.get("href").strip())
            #print(get_file_name(href))

    for pdf in pdflist:
        print(pdf)
        download_pdf(pdf)
        print("\n")
    print(len(pdflist))
