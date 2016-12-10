#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import datetime,time
from time import mktime
from orm import *
import signal

# class MyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return int(mktime(obj.timetuple()))
#         return json.JSONEncoder.default(self, obj)

def readPage(text):
    soup = BeautifulSoup(text,'lxml')
    jobElements = soup.find_all("article", class_="js_result_row")
    for jobElement in jobElements:
        # try:
            job = {}
            titleElement = jobElement.find("div", class_="jobTitle")
            link = titleElement.find("a")["href"]
            job["title"] = titleElement.find("a")["title"]
            job["link"] = link
            
            employerElement = jobElement.find("div", class_="company")
            companyLink = employerElement.find("a")
            if companyLink is not None:
                job["employer"] = companyLink["title"]
            else:
                companyText = employerElement.find("span", itemprop="name").getText()
                job["employer"] = companyText.replace("Found on: ","")
            address = {}
            cityElement = jobElement.find("span", itemprop="addressLocality")
            if cityElement is None:
                continue
            address["city"] = jobElement.find("span", itemprop="addressLocality").getText()
            address["province"] = jobElement.find("span", itemprop="addressRegion").getText()
            job["address"] = address
            dtstring = jobElement.find("time")["datetime"]
            dtstring = dtstring.split("T")[0]
            date = datetime.datetime.strptime(dtstring, "%Y-%m-%d")
            job["date"] = date
            job["month"] = date.date().month
            d1 = datetime.datetime.now()
            job["read_at"] = datetime.datetime.now()
            add_draft(job["read_at"], job["date"], job["month"], job["title"], job["employer"], job["address"]["province"], job["address"]["city"], job["link"])
        # except:
        #     print jobElement

create_draft_table()

driver = webdriver.PhantomJS()

urls = ["http://www.monster.ca/jobs/search/?q=.net-developer&where=canada&sort=dt.rv.di"]

for url in urls:
    driver.get(url)
    text = driver.page_source
    readPage(text)
    page_count = 0;
    while (page_count < 4):
        driver.find_element_by_xpath("//a[@class='page-link next']").click()
        try:
            page_count += 1
            print "read page NO: " + str(page_count)
            readPage(driver.page_source)
            time.sleep(3)
        except:
            print "some error occured, skip"
            continue
driver.service.process.send_signal(signal.SIGTERM)
driver.quit()
