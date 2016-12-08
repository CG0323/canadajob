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

def readPage(text):
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
        
        add_draft(job["date"], job["title"], job["employer"], job["address"]["province"], job["address"]["city"], job["link"])
    
create_draft_table()

driver = webdriver.PhantomJS()

urls = ["http://neuvoo.ca/jobs/?k=software+developer&l=quebec&f=24h&p=1&r=15&duc=&v=&source=", 
        "http://neuvoo.ca/jobs/?k=.net+developer&l=quebec&f=24h&p=1&r=15&duc=&v=&source="]

for url in urls:
    driver.get(url)
    text = driver.page_source
    readPage(text)
    page_count = 0;
    while (driver.find_element_by_xpath("//span[@class='page-next']/img").get_attribute('class') != "deactivated"):
        driver.find_element_by_xpath("//span[@class='page-next']").click()
        try:
            readPage(driver.page_source)
            page_count += 1
            if page_count > 10:
                break
        except:
            print "some error occured, skip"
            continue
driver.quit()
