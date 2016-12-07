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
                    title VARCHAR(50) NOT NULL,
                    employer VARCHAR(50) NOT NULL,
                    province VARCHAR(40),  
                    city VARCHAR(40), 
                    url VARCHAR(700),
                    PRIMARY KEY (title, employer), 
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
                    PRIMARY KEY (draft_id))"""
            cursor.execute(sql)
            cursor.execute('SET sql_notes = 1') 
            connection.commit()
    
    finally:
        connection.close();

def add_draft(post_at, title, employer, province, city, url):
    try:
        # Connect to the database
        print title + " from " + employer
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO draft (post_at,title,employer,province,city,url,refined) VALUES(%s,%s,%s,%s,%s,%s)"
            data = (post_at.strftime('%Y-%m-%d %H:%M:%S'),title,employer,province,city,url,False)
            cursor.execute(sql, data)
            connection.commit()
    except pymysql.DataError as error:
        code, message = error.args
        print ">>>>>>>>>>>>>", code, message
        connection.rollback()
    except:
        connection.rollback()
    finally:
        connection.close();

def get_test():
    try:
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM draft WHERE province = %s AND refined=%s"   
            
            cursor.execute(sql,("Quebec",False,))
            
            results = cursor.fetchall()
            for row in results:
                print row
    except:
        print ("Error: unable to fecth data")

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
            sql = "INSERT IGNORE INTO content (draft_id,content) VALUES(%s,%s)"
            data = (draft_id, content)
            cursor.execute(sql, data)
            connection.commit()
    # except pymysql.DataError as error:
    #     code, message = error.args
    #     print ">>>>>>>>>>>>>", code, message
    #     connection.rollback()
    # except:
    #     connection.rollback()
    finally:
        connection.close();