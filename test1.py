import sqlite3
import random

conn = sqlite3.connect('Coding101.db')
cursor = conn.cursor()

Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for i in Month:
	for j in range(23, 25):
		sql = """
INSERT INTO Borrowed_{}(Book_ID, User_ID, Whe_Finished, Page_SoFar)
VALUES({}, 1, 0, 20);
		""".format(i, j)
		cursor.execute(sql)
		conn.commit()

cursor.close()
conn.close()