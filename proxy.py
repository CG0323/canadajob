#!env/bin/python
#encoding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import *
import urllib2
import urllib
import socket

driver = webdriver.PhantomJS()

def get_proxies():
    try:
        proxies = []
        url = "http://gatherproxy.com/proxylist/country/?c=Canada"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,'lxml')
        tableElement = soup.find("table")
        rows = tableElement.findAll("tr")
        total = len(rows) - 1

        for i in range(2,total):
            row = rows[i]
            columns = row.findAll('td')
            proxies.append(columns[1].text + ":" + columns[2].text)
    # finally:
        driver.quit()
        print "found " + str(len(proxies)) + "candiate proxy ips"
        return proxies


def get_valid_proxies():
    candidate_proxies = get_proxies()
    url = "http://neuvoo.ca/"
    proxies = []
    socket.setdefaulttimeout(3)
    for i in range(0,len(candidate_proxies)):
        try:
            proxy_host = "http://"+candidate_proxies[i]
            proxy_temp = {"http":proxy_host}
            res = urllib.urlopen(url,proxies=proxy_temp).read()
            proxies.append(candidate_proxies[i])
            print "++++++found valid proxy ip: " + candidate_proxies[i]
        except Exception,e:
            print "------invalid proxy ip:" + candidate_proxies[i]
            continue
    return proxies


# driver = webdriver.PhantomJS()
# myProxy = "45.32.39.209:25"

# proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'httpProxy': myProxy, 'ftpProxy': myProxy, 'sslProxy': myProxy, 'noProxy':''})
# proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
# driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

# url = 'http://52.52.134.48:5000/'

# driver.get(url)
# time.sleep(3)
# print driver.page_source






