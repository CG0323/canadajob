#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime,time
from time import mktime
from orm import *
# from selenium.webdriver.support.ui import WebDriverWait


def cleanNeuvoo(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("div", id="job-container")
    if main is None:
        return None
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text

def cleanMonster(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("span", id="TrackingJobBody")
    if main is None:
        return None
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text

def cleanWorkopolis(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("section", class_="job-view-content-wrapper js-job-view-header-apply")
    if main is None:
        return None
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text

def cleanJoillico(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("div", class_="clr section jobrequirement")
    if main is None:
        return None
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text


def retrieve_content(draft):
    try:
        url = draft["url"]
        print url
        driver = webdriver.PhantomJS()
         #service_args=['--ignore-ssl-errors=true'])
        driver.get(url)
        while(url == driver.current_url or "job.php?" in driver.current_url):
            time.sleep(1)
        rurl = driver.current_url
        unknown = False
        if rurl.find("monster.ca") != -1:
            print "monster found!"
            # element = WebDriverWait(driver, 30).until(lambda x : x.find_element_by_id("TrackingJobBody"))
            text = cleanMonster(driver.page_source)
        elif rurl.find("workopolis") != -1:
            print "workopolis found!"
            # element = WebDriverWait(driver, 30).until(lambda x : x.find_element_by_class("job-view-content-wrapper js-job-view-header-apply"))
            text = cleanWorkopolis(driver.page_source)
        elif rurl.find("jobillico.com") != -1:
            print "jobillico found!"
            # element = WebDriverWait(driver, 30).until(lambda x : x.find_element_by_class("clr section jobrequirement"))
            text = cleanJoillico(driver.page_source)
        elif rurl.find("neuvoo.ca") != -1:
            print "neuvoo found!"
            # element = WebDriverWait(driver, 30).until(lambda x : x.find_element_by_id("job-container"))
            text = cleanNeuvoo(driver.page_source)
        else:
            unknown = True
        if text is not None:
            save_content(draft["id"], text)
            set_draft_refined(draft["id"], rurl)
        else:
            print "=======failed to load page====="
            print rurl
            print driver.page_source   
            print "==============================="
    finally:
        driver.quit()

drafts = get_drafts_by_province("Quebec")

create_content_table()
count = 1
for draft in drafts:
    print "handle draft No: " + str(count)
    count = count + 1
    retrieve_content(draft)