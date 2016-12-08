#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

# job  = cron.new(command='cd ~/canadajob;echo hello > ./test.txt')
jobs = []
for job in cron:
    jobs.append(job);
for job in jobs:
    cron.remove(job)

cron.write()
# job.minute.every(1)

# job.enable()
# cron.write()
# if cron.render():
#     print cron.render()