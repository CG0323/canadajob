#!./env/bin/python
import pymysql.cursors
import pymysql as my
import time 
import sys
from urllib import quote


def create_draft_table():
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SET sql_notes = 0') 
            sql = """CREATE TABLE IF NOT EXISTS draft ( 
                    id INT UNSIGNED NOT NULL auto_increment, 
                    post_at DATETIME,
                    read_at DATETIME,
                    month VARCHAR(10),
                    title VARCHAR(50) NOT NULL,
                    employer VARCHAR(50) NOT NULL,
                    province VARCHAR(40),  
                    city VARCHAR(40), 
                    url VARCHAR(700),
                    refined BOOLEAN,
                    rurl VARCHAR(700),
                    PRIMARY KEY (title, employer, month), 
                    KEY (id),
                    UNIQUE (url) )"""
            cursor.execute(sql)
            cursor.execute('SET sql_notes = 1') 
            connection.commit()
    
    finally:
        connection.close();

def create_content_table():
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SET sql_notes = 0') 
            sql = """CREATE TABLE IF NOT EXISTS content ( 
                    draft_id INT NOT NULL,
                    content TEXT,
                    analyzed BOOLEAN,
                    PRIMARY KEY (draft_id))"""
            cursor.execute(sql)
            cursor.execute('SET sql_notes = 1') 
            connection.commit()
    
    finally:
        connection.close();

def add_draft(read_at, post_at, month, title, employer, province, city, url):
    try:
        # Connect to the database
        print "add draft to db ============" + title + " from " + employer
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO draft (read_at,post_at,month,title,employer,province,city,url,refined) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (read_at.strftime('%Y-%m-%d %H:%M:%S'), post_at.strftime('%Y-%m-%d %H:%M:%S'),month,title,employer,province,city,url,False)
            cursor.execute(sql, data)
            connection.commit()
    finally:
        connection.close();

def get_drafts():  
    try:
        drafts = []
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM draft WHERE refined=%s"   
            
            cursor.execute(sql,(False,))
            
            results = cursor.fetchall()
            return results
    finally:
        connection.close();

def get_recent_drafts():  
    try:
        drafts = []
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM draft WHERE refined=%s AND read_at >=  NOW() - interval %s day"   
            
            cursor.execute(sql,(False,2))
            
            results = cursor.fetchall()
            return results
    finally:
        connection.close()

def get_new_valid_drafts():  
    try:
        drafts = []
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "select * from draft d where d.sent=false and d.id in (select draft_id from content);"   
            
            cursor.execute(sql)
            
            results = cursor.fetchall()
            return results
    finally:
        connection.close()

def get_drafts_by_province(province):  
    try:
        drafts = []
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM draft WHERE province = %s AND refined=%s"   
            
            cursor.execute(sql,(province,False,))
            
            results = cursor.fetchall()
            return results
    finally:
        connection.close();

def set_draft_refined(draft_id,rurl):  
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "UPDATE draft SET refined = 1, rurl = %s WHERE id = %s"
            cursor.execute(sql, (rurl, draft_id,))
            connection.commit()
    except:
        print "falied to update draft"
        connection.rollback()
    finally:
        connection.close();

def set_draft_sent(draft_id):  
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "UPDATE draft SET sent = 1 WHERE id = %s"
            cursor.execute(sql, (draft_id,))
            connection.commit()
    except:
        print "falied to update draft"
        connection.rollback()
    finally:
        connection.close();

def set_content_analyzed(draft_id):  
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "UPDATE content SET analyzed = 1 WHERE draft_id = %s"
            cursor.execute(sql, (draft_id,))
            connection.commit()
    except:
        print "falied to update content"
        connection.rollback()
    finally:
        connection.close();

def get_content_by_draft_id(draft_id):  
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM content WHERE draft_id=%s"  
            cursor.execute(sql, (draft_id,))
            results = cursor.fetchall()
            return results[0]
    except:
        print "falied to get content"
        connection.rollback()
    finally:
        connection.close();


def save_content(draft_id, content):
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO content (draft_id,content,analyzed) VALUES(%s,%s,%s)"
            data = (draft_id, content, False)
            cursor.execute(sql, data)
            connection.commit()
    finally:
        connection.close();

def get_contents():  
    try:
        contents = []
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM content WHERE analyzed=%s"   
            
            cursor.execute(sql,(False,))
            
            results = cursor.fetchall()
            return results
    finally:
        connection.close();

    
def create_skill_table():
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SET sql_notes = 0') 
            sql = """CREATE TABLE IF NOT EXISTS skill ( 
                    name VARCHAR(20) NOT NULL,
                    keywords VARCHAR(200),
                    is_reg BOOLEAN,
                    PRIMARY KEY (name))"""
            cursor.execute(sql)
            cursor.execute('SET sql_notes = 1') 
            connection.commit()
    
    finally:
        connection.close();

def add_skill(name, keywords, is_reg):
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO skill (name,keywords,is_reg) VALUES(%s,%s,%s)"
            data = (name, keywords, is_reg)
            cursor.execute(sql, data)
            connection.commit()
    finally:
        connection.close();

def create_job_table():
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SET sql_notes = 0') 
            sql = """CREATE TABLE IF NOT EXISTS job ( 
                    draft_id INT NOT NULL,
                    KEY (draft_id))"""
            cursor.execute(sql)
            cursor.execute('SET sql_notes = 1') 
            connection.commit()
    
    finally:
        connection.close();

def add_job(draft_id):
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO job (draft_id) VALUES(%s)"
            data = (draft_id)
            cursor.execute(sql, data)
            connection.commit()
    finally:
        connection.close();

def create_job_skill_table():
    try:
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SET sql_notes = 0') 
            sql = """CREATE TABLE IF NOT EXISTS job_skill ( 
                    draft_id INT NOT NULL,
                    skill VARCHAR(20) NOT NULL,
                    PRIMARY KEY (draft_id,skill))"""
            cursor.execute(sql)
            cursor.execute('SET sql_notes = 1') 
            connection.commit()
    
    finally:
        connection.close();

def add_job_skills(draft_id, skills):
    try:
        print "add skill for draft_id = " + str(draft_id) + " : " + ",".join(skills)
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO job_skill (draft_id,skill) VALUES(%s,%s)"
            for skill in skills:
                data = (draft_id, skill)
                cursor.execute(sql, data)
            connection.commit()
    finally:
        connection.close();

