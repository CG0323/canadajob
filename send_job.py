#!./env/bin/python
import requests
import json
from orm import *

url = 'http://60.205.216.128:8080/api/jobs'

jobs = get_new_valid_drafts()

for job in jobs:
    text = get_content_by_draft_id(job["id"])["content"].lower()
    content = {"text": text}
    data = {"readAt": job["read_at"], "postAt": job["post_at"], "title": job["title"], "employer":job["employer"], "province":job["province"], "city":job["city"], "url":job["rurl"], "content": content}
    r = requests.post(url, json = data)
    if r.status_code == requests.codes.ok:
      set_draft_sent(job.id)
