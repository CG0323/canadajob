#!./env/bin/python
VARCHAR(20)
import pymysql.cursors

def create_tables():
    # 执行sql语句
    try:
    # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='cg',
                                    password='088583-Salahdin',
                                    db='canadajob',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
        # 使用预处理语句创建表
        sql = """CREATE TABLE DRAFT IF NOT EXIST (
                POSTAT DATETIME,
                TITLE  VARCHAR(45),
                EMPLOYEE  VARCHAR(20),
                PROVINCE VARCHAR(20),  
                CITY VARCHAR(20), 
                URL VARCHAR(100) )"""

        cursor.execute(sql)
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    
    finally:
        connection.close();

