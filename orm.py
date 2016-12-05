#!./env/bin/python
import pymysql.cursors

# Connect to the database
db = pymysql.connect(host='localhost',
                             user='cg',
                             password='088583-Salahdin',
                             db='canadajob',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def create_tables():
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql = """CREATE TABLE DRAFT IF NOT EXIST (
            POSTAT DATETIME,
            TITLE  VARCHAR(45),
            EMPLOYEE  VARCHAR(20),
            PROVINCE VARCHAR(20),  
            CITY VARCHAR(20), 
            URL VARCHAR(100) )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()