#!./env/bin/python
import requests
import json
from orm import *

url = 'http://60.205.216.128:8080/api/skills'

jobs = get_new_valid_drafts()
print len(jobs)