import sqlite3
import utils as ext
import os

latestVersion = 51

def upgradeToLatest(plid):
	msg = ""
	if ext.checkVersion(plid) == 50:
		data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
		c = data.cursor()
		c.execute("""CREATE TABLE trades (tradeNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					tradeType TEXT NOT NULL,
					tradeDesc TEXT NOT NULL,
					tradeStatus TEXT NOT NULL,
					name TEXT NOT NULL,
					desc TEXT NOT NULL,
					type TEXT NOT NULL,
					tier TEXT NOT NULL,
					actions TEXT NOT NULL,
					del BOOLEAN,
					senderID TEXT NOT NULL,
					oiNum INTEGER NOT NULL)""")
		c.execute("ALTER TABLE inventory ADD COLUMN inTrade BOOLEAN")
		c.execute("UPDATE inventory SET inTrade=0")
		data.commit()
		data.close()
		ver = sqlite3.connect("lop.db")
		c = ver.cursor()
		c.execute("UPDATE players SET version=51 WHERE id=?", [plid])
		ver.commit()
		ver.close()
		msg = "Account upgraded to v.51\n"
	if not msg:
		return "You're already have the latest version"
	else:
		return msg
		