#!env/bin/python
# encoding: UTF-8
import json
import codecs
import re
from orm import *

def extractSkills(text, skillMap, skillReg, log):
    skills = []
    for (k,v) in skillMap.items():
        for keyword in v:
            if keyword in text:
                skills.append(k)
    for (k,v) in skillReg.items():
        pattern = re.compile(v)
        match = pattern.search(text)
        if match:
            skills.append(k)
    return skills

create_skill_table()


with open('skills.json') as infile:
    skillMap = json.load(infile)
    for (k,v) in skillMap.items():
        name = k
        keywords = ",".join(v)
        add_skill(name,keywords,False)
with open('skill-reg.json') as infile:
    skillReg = json.load(infile)
    for (k,v) in skillReg.items():
        name = k
        keywords = v
        add_skill(name,keywords,True)

create_job_table()
create_job_skill_table()
contents = get_contents()
print len(contents)


for content in contents:
    text = content["content"].lower()
    log = False
    skills = extractSkills(text,skillMap, skillReg,log)
    set_content_analyzed(content["draft_id"])
    if(len(skills) > 1):
        add_job(content["draft_id"])
        add_job_skills(content["draft_id"], skills)

