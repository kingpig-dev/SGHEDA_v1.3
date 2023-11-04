import sqlite3

def database_init(path):
    conn = sqlite3.connect(path)
    return conn



if __name__ == '__main__':
    conn = database_init('C/Program Files/SGHEDA/database/data.db')
    cursor = conn.cursor()
