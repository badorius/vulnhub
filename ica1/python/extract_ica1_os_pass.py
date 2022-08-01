import mysql.connector

try:
    connection = mysql.connector.connect(host='192.168.1.179',
                                         database='staff',
                                         user='qdpmadmin',
                                         password='UcVQCMQk2STVeS6J')

    sql_select_Query = "select id,name from user"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    # get all records
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)

    print("\nPrinting each row")
    for row in records:
        print("id = ", row[0], )
        print("name = ", row[1])

except mysql.connector.Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")