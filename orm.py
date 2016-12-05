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
            sql = """CREATE TABLE DRAFT ( POSTAT DATETIME,
                    TITLE VARCHAR(45),
                    EMPLOYEE VARCHAR(20),
                    PROVINCE VARCHAR(20),  
                    CITY VARCHAR(20), 
                    URL VARCHAR(100) )"""

            cursor.execute(sql)

            connection.commit()
    
    finally:
        connection.close();

