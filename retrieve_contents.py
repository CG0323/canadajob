#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime,time
from time import mktime
from orm import *


def cleanNeuvoo(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    print html
    main = soup.find("div", id="job-container")
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text

def cleanMonster(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("span", id="TrackingJobBody")
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text

def cleanWorkopolis(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("section", class_="job-view-content-wrapper js-job-view-header-apply")
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text

def cleanJoillico(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("div", class_="clr section jobrequirement")
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text


def retrieve_content(draft):
    try:
        url = draft["url"]
        driver = webdriver.PhantomJS()
        driver.get(url)
        rurl = driver.current_url
        unknown = False
        if rurl.find("neuvoo.ca") != -1:
            print "neuvoo found!"
            text = cleanNeuvoo(driver.page_source)
        elif rurl.find("monster.ca") != -1:
            print "monster found!"
            text = cleanMonster(driver.page_source)
        elif rurl.find("workopolis") != -1:
            print "workopolis found!"
            text = cleanWorkopolis(driver.page_source)
        elif rurl.find("jobillico.com") != -1:
            print "jobillico found!"
            text = cleanJoillico(driver.page_source)
        else:
            unknown = True
        set_draft_refined(draft["id"], rurl)
        save_content(draft["id"], text)
    finally:
        driver.quit()

drafts = get_drafts_by_province("Quebec")

create_content_table()
for draft in drafts:
    retrieve_content(draft)
    break