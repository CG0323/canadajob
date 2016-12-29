#!./env/bin/python
import requests
import json

url = 'http://60.205.216.128:8080/api/skills'

def push_skill(name, keywords, isReg):
    skill = {'name': name, 'keyWords':keywords, 'isReg': isReg}
    r = requests.post(url,json = skill)
    print r.text

requests.delete(url+'/all')

with open('skills.json') as infile:
    skillMap = json.load(infile)
    for (k,v) in skillMap.items():
        name = k
        keywords = ",".join(v)
        push_skill(name,keywords,False)
with open('skill-reg.json') as infile:
    skillReg = json.load(infile)
    for (k,v) in skillReg.items():
        name = k
        keywords = v
        push_skill(name,keywords,True)

r = requests.get(url)
print r.text