import sqlite3
import os
import requests, requests.exceptions
import commands as com
import importlib

def osuIsExist(id):
	data = sqlite3.connect("osuplayers.db")
	c = data.cursor()
	c.execute("SELECT * FROM players WHERE vkid=?", [id])
	if c.fetchone() is None:
		data.close()
		return False
	data.close()
	return True

def checkURL(url):
	while True:
		try:
			r = requests.get(url)
			if r.status_code != 200:
				return False
			return True
		except requests.exceptions.ConnectionError as e:
			return False
		except requests.exceptions.MissingSchema:
			url = "http://" + url
			continue

def toFixed(numObj, digits=0):
	return f"{numObj:.{digits}f}"

def dynamicImport(module):
	return importlib.import_module(module)

def numWithZero(number):
	if number < 10 and number > -1:
		return "0" + str(number)
	return number

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
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("SELECT inTradeZone FROM players WHERE id=?", [plid])
	if not int(c.fetchone()[0]):
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
	print(checkURL("хдд"))