#!./env/bin/python
VARCHAR(20)
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
                    TITLE CHAR(45),
                    EMPLOYEE CHAR(20),
                    PROVINCE CHAR(20),  
                    CITY CHAR(20), 
                    URL CHAR(100) )"""

            cursor.execute(sql)

            connection.commit()
    
    finally:
        connection.close();

