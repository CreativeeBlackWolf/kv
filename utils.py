import sqlite3
import os
import commands as com
import xml.etree.cElementTree as ET

def isExist(id):
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("SELECT * FROM players WHERE id=?", [id])
	if c.fetchone() is None:
		data.close()
		return False
	data.close()
	return True

def inInventory(plid, itemNumber):
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM inventory WHERE number=?", [itemNumber])
	if c.fetchone() is None:
		data.close()
		return False
	data.close()
	return True

def inTrade(plid, itemNumber):
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT inTrade FROM inventory WHERE number=?", [itemNumber])
	trade = c.fetchone()[0]
	if trade:
		data.close()
		return True
	data.close()
	return False

def inTradeZone(plid):
	coords = com.getCoords(plid)
	x = coords[0]
	y = coords[1]
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	for obj in root.findall("objectgroup"):
		if obj.attrib['name'] == "TradeZone":
			for trz in obj:
				if int(trz.attrib['x']) == x and int(trz.attrib['y']) == y:
					return True
	return False

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

def checkVersion(plid):
	if not isExist(plid):
		return False
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("SELECT version FROM players WHERE id=?", [plid])
	ver = c.fetchone()[0]
	data.close()
	return int(ver)

if __name__ == "__main__":
	pass
