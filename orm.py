#!./env/bin/python
import pymysql.cursors

def create_tables():
    try:
    # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = """CREATE TABLE IF NOT EXISTS draft ( post_at DATETIME,
                    title VARCHAR(45),
                    employee VARCHAR(20),
                    province VARCHAR(20),  
                    city VARCHAR(20), 
                    url VARCHAR(100) )"""

            cursor.execute(sql)

            connection.commit()
    
    finally:
        connection.close();

