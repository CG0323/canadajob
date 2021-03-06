#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import datetime,time
from time import mktime
from orm import *
from log_service import *

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)

def readPage(text):
    logger = get_logger()
    soup = BeautifulSoup(text,'lxml')
    jobElements = soup.find_all("div", class_="job-c")
    for jobElement in jobElements:
        try:
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
            job["read_at"] = d1
            if "d" in dateString:
                d = int(dateString.replace("d",""))
                job["date"] = d1 - datetime.timedelta(days=d)
            elif "h" in dateString:
                h = int(dateString.replace("h",""))
                job["date"] = d1 - datetime.timedelta(hours=h)
            job["month"] = job["date"].date().month
            
            add_draft(job["read_at"], job["date"], job["month"], job["title"], job["employer"], job["address"]["province"], job["address"]["city"], job["link"])
            logger.info("add draft to aws db, job title is:%s",job["title"])
        except Exception, e:
            logger.debug("[Neuvoo] Parse job element failed %s", e.message)

create_draft_table()

driver = webdriver.PhantomJS()

urls = ["http://neuvoo.ca/jobs/?k=software+developer&l=ottawa&f=24h&p=1&r=15&duc=&v=&source=","http://neuvoo.ca/jobs/?k=.NET+developer&l=ottawa&f=24h&p=1&r=15&duc=&v=&source=","http://neuvoo.ca/jobs/?k=Node.js+developer&l=ottawa&f=24h&p=1&r=15&duc=&v=&source="]

for url in urls:
    driver.get(url)
    js="var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    time.sleep(2)
    js_="var q=document.documentElement.scrollTop=0"
    driver.execute_script(js_)
    time.sleep(5)
    text = driver.page_source
    readPage(text)
    page_count = 0
    while (driver.find_element_by_xpath("//span[@class='page-next']/img").get_attribute('class') != "deactivated"):
        driver.find_element_by_xpath("//span[@class='page-next']").click()
        try:
            readPage(driver.page_source)
            page_count += 1
            if page_count > 6:
                break
        except:
            print "some error occured, skip"
            continue
driver.quit()
