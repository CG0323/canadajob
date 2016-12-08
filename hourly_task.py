#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime,time
from datetime import datetime
from time import mktime
from orm import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


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


def retrieve_content(driver,draft):
    try:
        url = draft["url"]
        print url
         #service_args=['--ignore-ssl-errors=true'])
        driver.set_page_load_timeout(30)
        driver.get(url)
        start = datetime.now()
        while(url == driver.current_url or "job.php?" in driver.current_url):
            time.sleep(1)
            if(datetime.now() - start).seconds > 20:
                break
        rurl = driver.current_url
        unknown = False
        text = None
        if rurl.find("monster.ca") != -1:
            print "monster found!"
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_id("TrackingJobBody"))
            text = cleanMonster(driver.page_source)
        elif rurl.find("workopolis") != -1 or rurl.find("click.appcast") != -1:
            # print "workopolis found! skip it"
            # text = None
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_css_selector(".job-view-content-wrapper.js-job-view-header-apply"))
            text = cleanWorkopolis(driver.page_source)
        elif rurl.find("jobillico.com") != -1:
            print "jobillico found!"
            # element = WebDriverWait(driver, 30).until(lambda x : x.find_element_by_class_name("clr section jobrequirement"))
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_css_selector(".clr.section.jobrequirement"))
            text = cleanJoillico(driver.page_source)
        elif rurl.find("neuvoo.ca") != -1:
            print "neuvoo found!"
            time.sleep(5)
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_id("job-container"))
            text = cleanNeuvoo(driver.page_source)
        else:
            unknown = True
        if text is not None:
            save_content(draft["id"], text)
        else:
            print "=======failed to load page====="
            print rurl
            print "==============================="
        set_draft_refined(draft["id"], rurl)
    except TimeoutException:
        set_draft_refined(draft["id"], "")
        print "time out occured"


drafts = get_recent_drafts()
create_content_table()
driver = webdriver.PhantomJS()
count = 1
total = len(drafts)
for draft in drafts:
    print "handle draft No: " + str(count) + "/" + str(total)
    count = count + 1
    retrieve_content(driver,draft)
    if count > 20:
        break
driver.quit()