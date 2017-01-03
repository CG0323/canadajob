#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import datetime,time
from time import mktime
from orm import *
import signal
from selenium.webdriver.support.ui import WebDriverWait
from log_service import *

# class MyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return int(mktime(obj.timetuple()))
#         return json.JSONEncoder.default(self, obj)


def readPage(text):
    logger = get_logger()
    soup = BeautifulSoup(text,'lxml')
    jobElements = soup.find_all("article", class_="js_result_row")
    for jobElement in jobElements:
        try:
            # print jobElement
            job = {}
            # titleElement = jobElement.find("div", class_="jobTitle")
            link = jobElement.find("a")["href"]
            job["title"] = jobElement.find("a")["title"]
            job["link"] = link
            
            employerElement = jobElement.find("div", class_="company")
            companyLink = employerElement.find("a")
            if companyLink is not None:
                job["employer"] = companyLink["title"]
            else:
                companyText = employerElement.find("span", itemprop="name").getText()
                job["employer"] = companyText.replace("Found on: ","")
            address = {}
            locationElement = jobElement.find("div", class_="location")
            
            adressStr = locationElement.find("span").getText()
            address["city"] = adressStr.split(",")[0]
            address["province"] = adressStr.split(",")[1]
            job["address"] = address

            dtstring = jobElement.find("time")["datetime"]
            d = dtstring.split(" ")[0]
            if d.isdigit() == False:
                d = "0"
            job["date"] = datetime.datetime.now() - datetime.timedelta(days=int(d))   
            job["month"] = job["date"].date().month
            job["read_at"] = datetime.datetime.now()
            add_draft(job["read_at"], job["date"], job["month"], job["title"], job["employer"], job["address"]["province"], job["address"]["city"], job["link"])
            logger.info("add draft to aws db, job title is:%s",job["title"])
        except:
            logger.error("Parse job element failed %s", jobElement)
create_draft_table()

driver = webdriver.PhantomJS()

urls = ["http://www.monster.ca/jobs/search/?q=.net-developer&where=canada&sort=dt.rv.di","http://www.monster.ca/jobs/search/?q=software-developer&where=canada"]



for url in urls:
    # element = WebDriverWait(driver, 25).until(lambda x : x.find_element_by_css_selector('span[itemprop="addressLocality"]'))
    for page in range (1,4):
        purl = url 
        if page > 1:
            purl = url + "&page=" + str(page)
        driver.get(purl)
        time.sleep(10)
        # element = WebDriverWait(driver, 20).until(lambda x : x.find_element_by_css_selector('span[itemprop="addressLocality"]'))
        # try:
        print "read page NO: " + str(page)
        readPage(driver.page_source)
        # except:
        #     print "some error occured when read menu page, skip"
        #     continue
driver.service.process.send_signal(signal.SIGTERM)
driver.quit()
