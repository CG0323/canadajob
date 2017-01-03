#!./env/bin/python
import requests
import json
from orm import *
import datetime,time

def send_job():
  url = 'http://60.205.216.128:8080/api/jobs'

  # requests.delete(url+'/all')
  # set_all_sent_false()
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
      title = title.replace(".NETDeveloper","")
      title = title.replace("Developer.NET","")
      title = title.replace("DeveloperDeveloper","Developer")
      employer = job["employer"].replace("Found on:","")
      data = {"readAt": read_at, "postAt": job["post_at"].strftime('%Y-%m-%d %H:%M:%S'), "title": title, "employer":employer, "province":job["province"], "city":job["city"], "url":job["rurl"], "content": content}
      r = requests.post(url, json = data)
      print "sent job id = " + str(job["id"])
      print r.status_code
      set_draft_sent(job["id"])


