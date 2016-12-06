#!./env/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime,time
from time import mktime
from orm import *

drafs = get_drafts_by_province('Quebec')
print drafs