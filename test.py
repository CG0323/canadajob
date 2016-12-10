#!./env/bin/python
#encoding=utf-8
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
r = requests.get("http://www.monster.ca/jobs/search/?q=software-developer&where=montreal")

soup = BeautifulSoup(r.content)
trs = soup.findAll('article', class_="js_result_row")
print trs
