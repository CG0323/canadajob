#!./env/bin/python
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='52.8.218.46',
                             user='cg',
                             password='088583-Salahdin',
                             db='canadajob',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('cg', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('cg',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()