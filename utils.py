import sqlite3
import os

def isExist(id):
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("SELECT * FROM players WHERE id=?", [id])
	if c.fetchone() is None:
		data.close()
		return False
	data.close()
	return True

def inFriends(plid, fid):
	data = sqlite3.connect(os.path.join('pl', f'{plid}.db'))
	c = data.cursor()
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	if c.fetchone() is None:
		return False
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	ans = c.fetchone()
	if ans[2] in ["Requested", "Request"]:
		return False
	return True
