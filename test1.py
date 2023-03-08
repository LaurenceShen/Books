import sqlite3
import random

conn = sqlite3.connect('Coding101.db')
cursor = conn.cursor()

Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for i in Month:
    sql = """
INSERT INTO Borrowed_{}(Book_ID, User_ID, Whe_Finished, Page_SoFar)
VALUES(1, 1, 1, 336);
    """.format(i)
    cursor.execute(sql)
    conn.commit()

cursor.close()
conn.close()