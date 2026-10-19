import sqlite3

def set_task(telegram_id:int | str, task: str):
    telegram_id = str(telegram_id)
    connect = sqlite3.connect("qwe.db")
    cursor = connect.cursor()

    cursor.execute("INSERT INTO users (login, tasks) VALUES (?,?)", (telegram_id, task))
    connect.commit()

    cursor.close()
    connect.close()

def get_task(telegram_id:int | str):
    telegram_id = str(telegram_id)
    connect = sqlite3.connect("qwe.db")
    cursor = connect.cursor()
    cursor.execute("SELECT id, tasks FROM users WHERE login = (?)", (telegram_id,))
    res= cursor.fetchall()
    cursor.close()
    connect.close()
    return res


def update_task(telegram_id: int | str, id: int | str, new_task: str):
    connect = sqlite3.connect("qwe.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET tasks = ? WHERE login = ? AND id = ?",(new_task, telegram_id, id))
    connect.commit()
    # cursor.execute("SELECT MAX (id) FROM users")
    # ids = cursor.fetchall()
    # max_id = int(ids[0][0])
    # if int(id) > max_id:

    cursor.close()
    connect.close()


def delete_task(telegram_id,id):
    connect = sqlite3.connect("qwe.db")
    cursor = connect.cursor()
    cursor.execute("DELETE FROM users WHERE login = ? AND id = ?",(telegram_id, id))
    connect.commit()

    cursor.close()
    connect.close()

if __name__ == "__main__":
    set_task(1036300774, "Задача1")
    set_task(1036300774, "Задача2")
    #update_task(1112345, 5, "1")
    print(get_task(1036300774))
        


#add_task(1112345,"1. Протестировать функцию add_task")

# connect = sqlite3.connect("qwe.db")
# cursor = connect.cursor()

# cursor.execute('''CREATE TABLE IF NOT EXISTS users(
#                id INTEGER PRIMARY KEY,
#                login TEXT UNIQE NOT NULL,
#                tasks TEXT
# )''')

# cursor.execute("INSERT INTO users (login, tasks) VALUES ('112332','1. Сделать базу данных')")
# connect.commit()

# cursor.close()
# connect.close()