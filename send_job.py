#!./env/bin/python
import requests
import json
from orm import *
import datetime,time

url = 'http://60.205.216.128:8080/api/jobs'

jobs = get_new_valid_drafts()

for job in jobs:
    text = get_content_by_draft_id(job["id"])["content"].lower()
    content = {"text": text}
    read_at = datetime.datetime.now()
    if job["read_at"] is not None:
      read_at = job["read_at"].strftime('%Y-%m-%d %H:%M:%S')
    data = {"readAt": read_at, "postAt": job["post_at"].strftime('%Y-%m-%d %H:%M:%S'), "title": job["title"], "employer":job["employer"], "province":job["province"], "city":job["city"], "url":job["rurl"], "content": content}
    r = requests.post(url, json = data)
    if r.status_code == requests.codes.ok:
      set_draft_sent(job.id)
