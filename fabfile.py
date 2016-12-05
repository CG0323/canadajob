#coding=utf-8
from __future__ import with_statement
from fabric.api import local, env, settings, abort, run, cd
from fabric.contrib.console import confirm
import time

# env.use_ssh_config = True
env.hosts = ['52.8.218.46']
env.user = 'ec2-user'
env.key_filename = '/users/wangchun/Downloads/development/cg007.pem'

# code_dir='/var/www/deploy-stage'
# app_dir='/var/www/application'
repo='https://github.com/CG0323/canadajob.git'
timestamp="release_%s" % int(time.time() * 1000)

def deploy():
    push()
    server_pull()

def push():
    local("git add --a")
    local("git commit -m 'auto commit with fabric'")
    local("git push")

def server_pull():
    with cd('~/canadajob'):   #cd用于进入某个目录
        run('git add --a') 
        run('git stash') 
        run('git pull')  #远程操作用run
        run('sudo chmod -R 777 ~/canadajob')
        
def install_modules():
    with cd('~/canadajob'):   #cd用于进入某个目录
        run('source env/bin/activate')
        run('pip install -r requirement.txt')



        


