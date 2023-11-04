import sqlite3
import json

connection = sqlite3.connect("../Logs/log/bin/data.db")
cursor = connection.cursor()

json_data = {
    'name': 'John Doe',
    'age': 25,
    'city': 'New York'
}

cursor.execute('INSERT INTO property (data) VALUES (?)', (json.dumps(json_data),))

connection.commit()

cursor.execute('select * from property')
rows = cursor.fetchall()

print(rows)