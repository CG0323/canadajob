#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import datetime,time
from time import mktime
from orm import *

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)

def readPage(text, jobs):
    soup = BeautifulSoup(text,'lxml')
    jobElements = soup.find_all("div", class_="job-c")
    for jobElement in jobElements:
        job = {}

        titleElement = jobElement.find("a", class_="gojob")
        link = titleElement["href"]
        spans = titleElement.find_all("span")
        jobTitle = ""
        for span in spans:
            jobTitle += span.getText()
        job["title"] = jobTitle
        job["link"] = "http://neuvoo.ca" + link;

        infoElement = jobElement.find("div", class_="j-info")
        employer = infoElement.find("span", itemprop="name").getText()
        job["employer"] = employer
        address = {}
        address["city"] = infoElement.find("span", itemprop="addressLocality").getText()
        address["province"] = infoElement.find("span", itemprop="addressRegion").getText()
        job["address"] = address
        dateString = infoElement.find("div", class_="j-date").getText()
        dateString = dateString.replace(" - ","")
        dateString = dateString.replace(" ago ","")
        d1 = datetime.datetime.now()
        if "d" in dateString:
            d = int(dateString.replace("d",""))
            job["date"] = d1 - datetime.timedelta(days=d)
        elif "h" in dateString:
            h = int(dateString.replace("h",""))
            job["date"] = d1 - datetime.timedelta(hours=h)
        jobs.append(job); 

url = 'http://neuvoo.ca/jobs/?k=.NET+Developer&l=montreal&f=&p=&r=';
# url = "www.163.com"
driver = webdriver.PhantomJS()
driver.get(url)
text = driver.page_source
jobs = []
readPage(text, jobs)
create_draft_table()
add_draft(jobs[0]["date"], jobs[0]["title"], jobs[0]["employer"], jobs[0]["address"]["city"], jobs[0]["address"]["province"], jobs[0]["link"])