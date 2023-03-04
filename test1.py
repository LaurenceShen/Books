import sqlite3
import random

conn = sqlite3.connect('Coding101.db')

cursor = conn.cursor()

Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
borrowed = {}
conn = sqlite3.connect('Coding101.db')
cursor = conn.cursor()
for i in Month:
    sql = """
SELECT * FROM Borrowed_{} INNER JOIN User ON User.ID = Borrowed_{}.User_ID
    """.format(i, i)
    cursor.execute(sql)
    borrowed_mon = cursor.fetchall()
    borrowed[i] = borrowed_mon

cursor.close()
conn.close()
for i in borrowed.items():
	print(i)