import sqlite3

def isExist(id):
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("SELECT * FROM players WHERE id=?", [id])
	if c.fetchone() is None:
		data.close()
		return False
	data.close()
	return True
