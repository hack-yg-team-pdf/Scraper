from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
import PyPDF2
import boto3
import json

S3PASSWORD = "AKIAJIBMWABVERJTH4PQ"
S3SECRET = "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"

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

        #remove password protection
##        with open(name, "rb") as openpdf:
##            pdf = PyPDF2.PdfFileReader(openpdf)
##            if pdf.isEncrypted:
##                pdf.decrypt("")
##                
##            if pdf.isEncrypted:
##                print(";(")

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
    #print(html.read())

    #create a list of all pdfs on the page
    soup = BeautifulSoup(html.read(), "html.parser")
    #print(soup.prettify())
    pdflist = []

    for forms in soup.find_all("p"):

        #check if the tag is under a category
        cat = ""
        try:
            group = forms.findPreviousSibling("h3")
            groupname = group.findChild("strong").contents
            for catname in groupname: 
                cat = catname
        except(AttributeError):
            None
        print(cat)

        #if there is a category
        if cat:

        
        #get the links from the anchor tags

        #for form in
##        href = link.get("href")
##
##        #strip the href string and check the last for characters for .pdf
##        if href and href.strip()[-4:] == ".pdf":
##            print(parent.get_text()[:10])
##            print("\n")
##            pdflist.append(href.strip())
##            #print(link.get("href").strip())
##            #print(get_file_name(href))

##    #download all of the pdfs
##    missinglist = []
##    for pdf in pdflist:
##        #print(pdf)
##        download_pdf(pdf, missinglist)
##        #print("\n")
##
##    if missinglist:
##        for e404 in missinglist:
##            pdflist.remove(e404)
##
##    #create S3 session
##    session = boto3.Session(
##        aws_access_key_id = S3PASSWORD,
##        aws_secret_access_key = S3SECRET)
##    s3 = session.resource("s3")
##    #bucket_list = [bucket.name for bucket in s3.buckets.all()]
##    #print(bucket_list)
##    
##    
##    #bindata = b"data"
##    #testobj = s3.Object("yg-pdf", "raw_pdfs/testbindata")
##    #testobj.put(Body = bindata)
##    
##    #upload all of the pdfs to S3
##    for pdf in pdflist:
##        upload_pdf(pdf, s3)
##        print(get_file_name(pdf) + " has been uploaded")
##
##    bucket = s3.Bucket("yg-pdf")
##    for obj in bucket.objects.all():
##        print(obj)
##        
    print(len(pdflist))
