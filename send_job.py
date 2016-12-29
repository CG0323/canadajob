#!./env/bin/python
import requests
import json
from orm import *
import datetime,time

url = 'http://60.205.216.128:8080/api/jobs'

requests.delete(url+'/all')
set_all_sent_false()
jobs = get_new_valid_drafts()

for job in jobs:
    text = get_content_by_draft_id(job["id"])["content"].lower()
    content = {"text": text}
    read_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if job["read_at"] is not None:
      read_at = job["read_at"].strftime('%Y-%m-%d %H:%M:%S')
    title = job["title"]
    title = title.replace(".NetDeveloper","")
    title = title.replace("Developer.Net","")
    title = title.replace("DeveloperDeveloper","Developer")
    data = {"readAt": read_at, "postAt": job["post_at"].strftime('%Y-%m-%d %H:%M:%S'), "title": title, "employer":job["employer"], "province":job["province"], "city":job["city"], "url":job["rurl"], "content": content}
    r = requests.post(url, json = data)
    print r.text
    set_draft_sent(job["id"])
    #   if r.status_code == requests.codes.ok:
    #     print "successfull sent job " + job["title"]
    #     set_draft_sent(job.id)
    #   else:
    #     print "!!failed sent job " + job["title"]
    # except:
    #     print "exception occured"

