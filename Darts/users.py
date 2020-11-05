import mysql.connector


def db_connect(db_name=""):
    """Function to make connection to database"""
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "auth_plugin": "mysql_native_password",
        "database": f"{db_name}"
    }
    c = mysql.connector.connect(**config)
    try:
        c = mysql.connector.connect(**config)
        return c
    except:
        print("Connection Error")
        exit(1)


def dbs_show(db_name=""):
    """Function to show all existing databases"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    my_cursor.execute("SHOW DATABASES")
    return [db[0].decode("utf-8") for db in my_cursor]


def tbls_show(db_name):
    """Function to show all tables within database"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    my_cursor.execute("SHOW TABLES;")
    return [tbl[0].decode("utf-8") for tbl in my_cursor]


def db_create(db_name):
    cn = db_connect()
    my_cursor = cn.cursor()
    my_cursor.execute(f"CREATE DATABASE {db_name}")


def db_remove(db_name):
    cn = db_connect()
    my_cursor = cn.cursor()
    my_cursor.execute(f"DROP DATABASE {db_name}")


def tbl_create(tbl_name, db_name=""):
    """Function to create a table within a chosen database"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    my_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tbl_name} (
        nick            VARCHAR(255),
        highest_score   INTEGER(10)     DEFAULT 0,
        games_played    INTEGER(10)     DEFAULT 0,
        games_won       INTEGER(10)     DEFAULT 0,
        games_lost      INTEGER(10)     DEFAULT 0,
        user_id         INT AUTO_INCREMENT PRIMARY KEY
    )""")


def tbl_drop(tbl_name, db_name=""):
    """Function to drop a table within a chosen database"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    my_cursor.execute(f"DROP TABLE {tbl_name}")


# print(tbl_create("darts_users", "darts"))
# print(tbls_show("darts"))


def add_user(nick, tbl_name, db_name):
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    sql_command = f"INSERT INTO {tbl_name} (nick) VALUES ('{nick}')"
    my_cursor.execute(sql_command)
    cn.commit()


def select_user(nick, tbl_name, db_name):
    """Function to select an user from a database"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    sql_command = f"SELECT * FROM {tbl_name}"
    my_cursor.execute(sql_command)
    return [user for user in my_cursor]


def delete_user(nick, tbl_name, db_name):
    """Function to remove an user from a database"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    sql_command = f"DELETE FROM {tbl_name} WHERE nick='{nick}'"
    my_cursor.execute(sql_command)
    cn.commit()


def tbl_column_counter(tbl_name, db_name):
    """Function to remove an user from a database"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    sql_command = f"SELECT count(*) FROM information_schema.columns WHERE table_name = '{tbl_name}'"
    my_cursor.execute(sql_command)
    return my_cursor.__next__()[0]


def tbl_change_order(tbl_name, db_name):
    """Function to remove an user from a database"""
    cn = db_connect(db_name)
    my_cursor = cn.cursor()
    sql_command = f"ALTER TABLE {tbl_name} MODIFY COLUMN games_lost INTEGER(10) AFTER games_won;"
    my_cursor.execute(sql_command)
    cn.commit()

#
# tbl_change_order("darts_users", "darts")