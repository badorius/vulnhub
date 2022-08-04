import mysql.connector
import base64


def mysql_select():
    try:
        connection = mysql.connector.connect(host='192.168.1.179',
                                            database='staff',
                                            user='qdpmadmin',
                                            password='UcVQCMQk2STVeS6J')


        sql_select_Query = "select * from user join login using (id);"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()

        for row in records:
            uncpass = base64.b64decode(row[5])
            print(row[2], uncpass)

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


def main():
    mysql_select()


if __name__ == "__main__":
    main()
