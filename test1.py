import sqlite3

conn = sqlite3.connect('Coding101.db')

cursor = conn.cursor()
cursor.execute("SELECT * FROM User;")

record = cursor.fetchall()
for i in range(1, 4):
	sql = """
DELETE FROM User WHERE ID = {}
	""".format(i)
	print(sql)
	cursor.execute(sql)
	conn.commit()

cursor.close()
conn.close()