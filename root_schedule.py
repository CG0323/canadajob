#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_reboot = cron.new(command='/sbin/reboot',comment='job_reboot1')

job_reboot.minute.on(26)
job_reboot.hour.on(3)
job_reboot.enable()

job_reboot = cron.new(command='/sbin/reboot',comment='job_reboot2')

job_reboot.minute.on(37)
job_reboot.hour.on(6)
job_reboot.enable()

job_reboot = cron.new(command='/sbin/reboot',comment='job_reboot3')

job_reboot.minute.on(26)
job_reboot.hour.on(9)
job_reboot.enable()

job_reboot = cron.new(command='/sbin/reboot',comment='job_reboot4')

job_reboot.minute.on(11)
job_reboot.hour.on(12)
job_reboot.enable()

job_reboot = cron.new(command='/sbin/reboot',comment='job_reboot5')

job_reboot.minute.on(09)
job_reboot.hour.on(15)
job_reboot.enable()

job_reboot = cron.new(command='/sbin/reboot',comment='job_reboot6')

job_reboot.minute.on(12)
job_reboot.hour.on(19)
job_reboot.enable()


cron.write()
cron.render()