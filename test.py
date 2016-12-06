#!/usr/local/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import json

def cleanNeuvoo(html):
    soup = BeautifulSoup(html,"lxml") # create a new bs4 object from the html data loaded
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




with open('menu.txt') as infile:
    jobs = json.load(infile)

for i in range(0,19):
    try:
        url = jobs[i]["link"]
        driver = webdriver.Chrome()
        driver.get(url)
        current_url = driver.current_url
        unknown = False
        if current_url.find("neuvoo.ca") != -1:
            print "neuvoo found!"
            text = cleanNeuvoo(driver.page_source)
        elif current_url.find("monster.ca") != -1:
            print "monster found!"
            text = cleanMonster(driver.page_source)
        elif current_url.find("workopolis") != -1:
            print "workopolis found!"
            text = cleanWorkopolis(driver.page_source)
        elif current_url.find("jobillico.com") != -1:
            print "jobillico found!"
            text = cleanJoillico(driver.page_source)
        else:
            unknown = True
    finally:
        driver.quit()





