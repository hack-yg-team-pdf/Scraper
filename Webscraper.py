from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
import boto3
import json

S3PASSWORD = "

def get_file_name(file_string):
    
    #return a string of everything after the last "/"
    return file_string[file_string.rfind("/")+1:]

def download_pdf(url, msnglst):
    
    #download the file specified in the argument, assume it's a PDF
    
    #Remove passwords if possible
    try:
        #open the url
        pdf_file = urlopen(url)
        
        #get the file name
        name = get_file_name(url)
        print(name)
        
        #create a binary writable file with the name of the pdf
        file = open(name, "wb")
        
        #write and close the file
        file.write(pdf_file.read())
        file.close()

        #handle errors
    except urllib.error.HTTPError:
        name = get_file_name(url)
        errmsg = " could not be found."
        print(name + errmsg)
        msnglst.append(url)

def upload_pdf(url, s3):

    #get the file name
    name = get_file_name(url)

    #upload the file
    s3.Bucket("yg-pdf").upload_file(name, f"raw_pdfs/{name}")
    

if __name__ == "__main__":
    
    #open the webpage
    html = urlopen("http://www.gov.yk.ca/forms/all.html")

    #create a list of all pdfs on the page
    soup = BeautifulSoup(html.read(), "html.parser")
    #print(soup.prettify())
    pdflist = []
    manifest = {"form categories":[]}
    catid = 0

    for forms in soup.find_all("p"):

        #check if the tag is under a category
        cat = ""
        try:
            #check if there is a category
            group = forms.findPreviousSibling("h3")
            groupname = group.findChild("strong").contents
            for catname in groupname: 
                cat = catname
        except(AttributeError):
            None
        #print("\n")
        #print(cat)

        #if there is a category, get the description
        if cat:        
            desc = ""
            for string in forms.stripped_strings:
                if not desc:
                    desc = string
            #print(desc)

            for link in forms.findChildren("a"):

                #get the links from the anchor tags
                href = link.get("href")
                if href and href.strip()[-4:] == ".pdf":
                    pdflist.append(href.strip())

                    #create the manifest entry

                    #check if the category already exists, and add it
                    #if it doesn't
                    exists = 0
                    for category in manifest["form categories"]:
                        if category["name"] == cat:
                            exists = 1
                            break
                    if not exists:
                        manifest["form categories"].append({"id":catid, "name": cat, "fileinfo": []})
                        catid += 1
                        
                     #find the category and add the entry
                    for category in manifest["form categories"]:
                        if category["name"] == cat:
                            category["fileinfo"].append(
                                {"description": desc,
                                "pdf": href.strip(),
                                 "json": get_file_name(href.strip())[:-4] + ".json"})


    #download all of the pdfs
    missinglist = []
    for pdf in pdflist:
        print(pdf)
        download_pdf(pdf, missinglist)
        #print("\n")

    if missinglist:
        for e404 in missinglist:
            pdflist.remove(e404)

            #remove not found files from the manifest
            #name = get_file_name(e404)
            for cat in manifest["form categories"]:
                for i in range(len(cat["fileinfo"])):
                    if cat["fileinfo"][i]["pdf"] == e404:
                        del cat["fileinfo"][i]
                        break

    #output the manifest
    with open("manifest.json", "w") as outfile:
        json.dump(manifest, outfile)                  

    #create S3 session
    session = boto3.Session(
        aws_access_key_id = S3PASSWORD,
        aws_secret_access_key = S3SECRET)
    s3 = session.resource("s3")
    
##    #upload all of the pdfs to S3
##    for pdf in pdflist:
##        upload_pdf(pdf, s3)
##        print(get_file_name(pdf) + " has been uploaded")

    #upload the manifest
    s3.Bucket("yg-pdf").upload_file("manifest.json", f"raw_pdfs/manifest.json")
    print("Manifest uploaded")
        
    #print(len(pdflist))
