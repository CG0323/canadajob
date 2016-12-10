#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_reboot = cron.new(command='/sbin/reboot',comment='job_reboot')

job_reboot.minute.on(26)
job_reboot.hour.on(3)
job_reboot.enable()


cron.write()
cron.render()