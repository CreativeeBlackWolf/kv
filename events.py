import commands as com
import xml.etree.cElementTree as ET
import random
import os
import gi
import sqlite3

events = ["test"]

def createEvent(plid):
	tree = ET.parse("session.tmx")
	pos = com.getCoords(plid)
	root = tree.getroot()
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == "Triggers":
			ev = random.choice(events)
			if ev == 'test':
				ET.SubElement(i, 'object', {"name": "eventTest", "type": "test", "x": str(pos[0]), "y": str(pos[1]), 'width': '1', 'height': '1'})
				text = event_Test()
	tree.write('session.tmx', 'UTF-8')
	return text

def spawnMerchant(plid):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	coords = com.getCoords(plid)
	x = coords[0]
	y = coords[1]
	for i in root.findall("objectgroup"):
		if i.attrib['name'] == "Merchants":
			ET.SubElement(i, "object", {"name": "Merchant", "type": "uncheckedMerchant", "x": x, "y": y, "width": '1', 'height': '1'})
			data = sqlite3.connect(os.path.join("npc", f"merchant-{x}{y}.db"))
			c = data.cursor()
			c.execute("""CREATE TABLE inventory (number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL,
					desc TEXT NOT NULL,
					type TEXT NOT NULL,
					tier TEXT NOT NULL,
					actions TEXT NOT NULL,
					del BOOLEAN NOT NULL,
					price INTEGER NOT NULL)""")
			c.execute("CREATE TABLE spList (name TEXT NOT NULL, price INTEGER NOT NULL)")
			data.commit()			
			data.close()
			gen = gi.Item(plid)
			for i in range(random.randint(3, 7)):
				gen.addMerchantItem([x, y], "Common", "Uncommon", "Rare")
			tree.write("session.tmx", "UTF-8")
			return "Here is the Merchant"

def fillMerchant(plid):
	pass

def genChest(plid):
	chest = random.randint(0, 100)
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	coords = com.getCoords(plid)
	x = coords[0]
	y = coords[1]
	for i in root.findall("objectgroup"):
		if i.attrib['name'] == "Chests":
			if chest <= 60:
				ET.SubElement(i, 'object', {"name": "Chest", "type": "ClosedStandart", "x": x, "y": y, 'width': '1', 'height': '1'})
				chestType = "Standart"
			elif chest <= 80:
				ET.SubElement(i, 'object', {"name": "Chest", "type": "ClosedRare", "x": x, "y": y, 'width': '1', 'height': '1'})
				chestType = "Rare"
			elif chest <= 95:
				ET.SubElement(i, 'object', {"name": "Chest", "type": "ClosedExclusive", "x": x, "y": y, 'width': '1', 'height': '1'})
				chestType = "Exclusive"
			elif chest <= 100:
				ET.SubElement(i, 'object', {"name": "Chest", "type": "ClosedAbsolute", "x": x, "y": y, 'width': '1', 'height': '1'})
				chestType = "Absolute"
	tree.write('session.tmx', 'UTF-8')
	return "Here is the Closed {} chest".format(chestType)

def event_Test():
	return "пiпався"

if __name__ == "__main__":
	print(spawnMerchant(409541670))