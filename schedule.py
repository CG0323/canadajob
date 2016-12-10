#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_menu  = cron.new(command='cd ~/canadajob;source env/bin/activate;./monster.py',comment='job_menu')

job_menu.minute.on(32)
job_menu.hour.on(3)
job_menu.enable()

job_content = cron.new(command='cd ~/canadajob;source env/bin/activate;./hourly_task.py',comment='job_content')

job_content.minute.on(39)
job_content.hour.on(3)
job_content.enable()

cron.write()
cron.render()