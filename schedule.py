#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_daily = cron.new(command='sudo su; /sbin/reboot',comment='job_reboot')

job_daily.minute.on(2)
job_daily.hour.on(7)
job_daily.enable()

job_reboot  = cron.new(command='cd ~/canadajob;source env/bin/activate;./daily_task.py',comment='job_menu')

job_reboot.minute.on(8)
job_reboot.hour.on(7)
job_reboot.enable()

job_hourly = cron.new(command='cd ~/canadajob;source env/bin/activate;./hourly_task.py',comment='job_content')

job_hourly.minute.on(16)
job_hourly.hour.on(7)
job_hourly.enable()

cron.write()
cron.render()