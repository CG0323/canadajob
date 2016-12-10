#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_menu1  = cron.new(command='cd ~/canadajob;source env/bin/activate;./monster.py',comment='job_monster')

job_menu1.minute.on(02)
job_menu1.hour.on(8)
job_menu1.enable()


# job_menu2  = cron.new(command='cd ~/canadajob;source env/bin/activate;./daily_task.py',comment='job_neuvoo')

# job_menu2.minute.on(10)
# job_menu2.hour.on(8)
# job_menu2.enable()

job_content = cron.new(command='cd ~/canadajob;source env/bin/activate;./hourly_task.py',comment='job_content')

job_content.every_reboot()

cron.write()
cron.render()