#!./env/bin/python
import pymysql.cursors
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
                    title VARCHAR(45),
                    employer VARCHAR(20),
                    province VARCHAR(20),  
                    city VARCHAR(20), 
                    url VARCHAR(600),
                    PRIMARY KEY (id), 
                    UNIQUE (url) )"""
            cursor.execute(sql)
            cursor.execute('SET sql_notes = 1') 
            connection.commit()
    
    finally:
        connection.close();

def add_draft(post_at, title, employer, province, city, url):
    try:
        print "i am adding"
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        print "i am adding 1"
        with connection.cursor() as cursor:
            sql = "INSERT INTO draft (post_at,title,employer,province,city,url) VALUES(%s,%s,%s,%s,%s,%s)"
            print "i am adding 2"
            data = (post_at.strftime('%Y-%m-%d %H:%M:%S'),title,employer,province,city,quote(url));
            print data
            cursor.execute(sql, data)
            connection.commit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        connection.rollback()
    finally:
        
        connection.close();

