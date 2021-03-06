#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime,time
from datetime import datetime
from time import mktime
from orm import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from proxy import *
from selenium.webdriver.common.proxy import *
import signal
import socket
import random
from send_job import *
from log_service import *



def cleanNeuvoo(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("div", id="job-container")
    if main is None:
        return None
    for script in main(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    text ="\n".join(main.strings)
    return text

def cleanMonsterOpening(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
    main = soup.find("div", class_="jobview-section")
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


def retrieve_content(driver,draft,logger):
    try:
        url = draft["url"]
        logger.debug(url)
         #service_args=['--ignore-ssl-errors=true'])
        driver.set_page_load_timeout(30)
        driver.get(url)
        # start = datetime.now()
        # while(url == driver.current_url or "job.php?" in driver.current_url):
        #     time.sleep(1)
        #     if(datetime.now() - start).seconds > 20:
        #         break
        rt = random.randint(15, 50)
        time.sleep(rt)
        rurl = driver.current_url
        unknown = False
        text = None
        time.sleep(2)
        js="var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(2)

        js_="var q=document.documentElement.scrollTop=0"
        driver.execute_script(js_)
        time.sleep(5)

        if rurl.find("job-openings.monster") != -1:
            logger.debug("monster opening found!")
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_css_selector(".jobview-section"))
            text = cleanMonsterOpening(driver.page_source)
        elif rurl.find("monster.ca") != -1:
            logger.debug("monster found!")
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_id("TrackingJobBody"))
            text = cleanMonster(driver.page_source)
        elif rurl.find("workopolis") != -1 or rurl.find("click.appcast") != -1:
            # print "workopolis found! skip it"
            # text = None
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_css_selector(".job-view-content-wrapper.js-job-view-header-apply"))
            text = cleanWorkopolis(driver.page_source)
        elif rurl.find("jobillico.com") != -1:
            logger.debug("jobillico found!")
            # element = WebDriverWait(driver, 30).until(lambda x : x.find_element_by_class_name("clr section jobrequirement"))
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_css_selector(".clr.section.jobrequirement"))
            text = cleanJoillico(driver.page_source)
        elif rurl.find("neuvoo.ca") != -1:
            logger.debug("neuvoo found!")
            element = WebDriverWait(driver, 5).until(lambda x : x.find_element_by_id("job-container"))
            text = cleanNeuvoo(driver.page_source)
        else:
            unknown = True
        if text is not None:
            save_content(draft["id"], text)
        else:
            logger.error("=======failed to load page=====")
            logger.error(rurl)
            logger.error("===============================")
        set_draft_refined(draft["id"], rurl)
    except TimeoutException:
        set_draft_refined(draft["id"], "")    
        logger.error("time out occured, url is: %s",url)


time.sleep(120) # wait 2 minutes after reboot
driver = webdriver.PhantomJS()
# myProxy = "192.99.128.170:3128"
# proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'httpProxy': myProxy, 'ftpProxy': myProxy, 'sslProxy': myProxy, 'noProxy':''})
# proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
# print webdriver.DesiredCapabilities.PHANTOMJS
# driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

drafts = get_recent_drafts()
create_content_table()
count = 1
total = min(len(drafts),15)
logger = get_logger()

for i in range(0,total - 1):
    logger.debug("handle draft No: " + str(count) + "/" + str(total))
    count = count + 1
    try:
        retrieve_content(driver,drafts[i], logger)
    finally:
        time.sleep(30)
driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
driver.quit()
send_job()