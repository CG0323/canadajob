#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_reboot = cron.new(command='sudo su; /sbin/reboot',comment='job_reboot')

job_reboot.minute.on(2)
job_reboot.hour.on(7)
job_reboot.enable()

job_menu  = cron.new(command='cd ~/canadajob;source env/bin/activate;./daily_task.py',comment='job_menu')

job_menu.minute.on(8)
job_menu.hour.on(7)
job_menu.enable()

job_content = cron.new(command='cd ~/canadajob;source env/bin/activate;./hourly_task.py',comment='job_content')

job_content.minute.on(8)
job_content.hour.on(8)
job_content.enable()

cron.write()
cron.render()