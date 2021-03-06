import xml.etree.cElementTree as ET
import sqlite3
import os
import events
import utils as ext
import commands as com
import vk_api
import random
import gi

with open('token.txt', 'r') as f:
	token = f.read()
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

def move(plid, direction):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	oldcoords = com.getCoords(plid)
	
	for objects in root.findall('objectgroup[@name="Players"]'):
		for m in objects:
			if m.attrib['name'] == str(plid):
				if direction == "left":
					x = int(m.attrib['x']) - 1
					if x < 0:
						return "You can't move left anymore"
					m.set('x', str(x))
				if direction == "right":
					x = int(m.attrib['x']) + 1
					m.set('x', str(x))
				if direction == "up":
					y = int(m.attrib['y']) - 1
					if y < 0:
						return "You can't move up anymore."
					m.set('y', str(y))
				if direction == "down":
					y = int(m.attrib['y']) + 1
					m.set('y', str(y))
				print(f"{plid} moved: {oldcoords[0]};{oldcoords[1]} -> {m.attrib['x']};{m.attrib['y']}")
	
	for i in root.findall('objectgroup[@name="Players"]'):
		for players in i:
			if int(players.attrib['x']) == int(oldcoords[0]) and int(players.attrib['y']) == int(oldcoords[1]):
				if players.attrib['name'] != plid:	
					vk.messages.send(random_id=0, user_id=players.attrib['name'], message=f"{com.searchByID(plid)} has left from your square.")

	tree.write('session.tmx', 'UTF-8')
	tr = eventTrigger(plid)
	return f"You moved {direction}\n\n{tr}"

def chat(plid, msg, action=False):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	pos = com.getCoords(plid)
	msg = f"{' '.join(msg)}"
	x = int(pos[0])
	y = int(pos[1])
	for i in root.findall('objectgroup[@name="Players"]'):
		for players in i:
			if int(players.attrib['x']) == x and int(players.attrib['y']) == y:
				if not action:
					vk.messages.send(random_id=0, user_id=players.attrib['name'], message=f"{com.searchByID(plid)}: {msg}")
				else:
					vk.messages.send(random_id=0, user_id=players.attrib['name'], message=f"{com.searchByID(plid)} {msg}")

def openChest(plid):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	pos = com.getCoords(plid)
	x = int(pos[0])
	y = int(pos[1])
	for i in root.findall('objectgroup[@name="Chests"]'):
		for chests in i:
			if int(chests.attrib['x']) == x and int(chests.attrib['y']) == y:
				item = gi.Item(plid)
				if chests.attrib['type'] == 'ClosedStandart':
					i.remove(chests)
					tree.write("session.tmx", "UTF-8")
					return item.addItem("Common", "Uncommon")
				if chests.attrib['type'] == 'ClosedRare':
					i.remove(chests)
					tree.write("session.tmx", "UTF-8")
					return item.addItem("Uncommon", "Rare")
				if chests.attrib['type'] == 'ClosedExclusive':
					i.remove(chests)
					tree.write("session.tmx", "UTF-8")
					return item.addItem("Rare", "Exclusive")
				if chests.attrib['type'] == 'ClosedAbsolute':
					i.remove(chests)
					tree.write("session.tmx", "UTF-8")
					return item.addItem("Absolute")
	return "There're no chests here"

def itemAction(plid, itemNumber):
	if not ext.inInventory(plid, itemNumber):
		return "Wrong item number. Check your inventory again"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM inventory WHERE number=?", [itemNumber])
	item = c.fetchone()
	actions = item[5].split(" | ")
	msg = ""
	if item[6]:
		msg += f"{item[1]} has been deleted from inventory\n"
		c.execute("DELETE FROM inventory WHERE number=?", [itemNumber])
		data.commit()
	msg += random.choice(actions)
	if item[1] == "Cassette" and msg.startswith('These two holes remind you of eyes'):
		c.execute("SELECT * FROM friends WHERE name='Cassette'")
		if c.fetchone() is None:
			msg += "\n\nCassette was added to your friend list"
			c.execute("INSERT INTO friends VALUES ('???', 'Cassette', 'Accepted')")
			data.commit()
		else:
			pass
	data.close()
	return msg

def eventTrigger(plid):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	pos = com.getCoords(plid)
	x = int(pos[0])
	y = int(pos[1])
	text = ""
	for i in root.findall('objectgroup[@name="Players"]'):
		for players in i:
			if int(players.attrib['x']) == x and int(players.attrib['y']) == y:
				if players.attrib['name'] != str(plid):
					vk.messages.send(random_id=0, user_id=players.attrib['name'], message=f"The {com.searchByID(plid)} has come.")
					text = "There're some players on this position"

	for i in root.findall('objectgroup[@name="Triggers"]'):
		for triggers in i:
			if int(triggers.attrib['x']) == x and int(triggers.attrib['y']) == y:
				trtype = triggers.attrib['type']
				if trtype == "test":
					i.remove(triggers)
					tree.write('session.tmx', 'UTF-8')
					text = text + f"\n{events.event_Test()}"
					break

	for i in root.findall('objectgroup[@name="Chests"]'):
		for chests in i:
			if int(chests.attrib['x']) == x and int(chests.attrib['y']) == y:
				chtype = chests.attrib['type']
				if chtype == "ClosedStandart":
					text = "Here is the Closed Standart chest"
				elif chtype == "ClosedRare":
					text = "Here is the Closed Rare chest"
				elif chtype == "ClosedExclusive":
					text = "Here is the Closed Exclusive chest"
				else:
					text = "Here is the Closed Absolute chest"
				break

	for i in root.findall('objectgroup[@name="Merchants"]'):
		for m in i:
			if int(m.attrib['x']) == x and int(m.attrib['y']) == y:
				text = "Here is the Merchant"
				break

	itz = False
	for i in root.findall('objectgroup[@name="TradeZones"]'):
		for tz in i:
			if int(tz.attrib['x']) == x and int(tz.attrib['y']) == y:
				data = sqlite3.connect("lop.db")
				c = data.cursor()
				c.execute("SELECT inTradeZone FROM players WHERE id=?", [plid])
				if int(c.fetchone()[0]) == 0:
					c.execute("UPDATE players SET inTradeZone=1 WHERE id=?", [plid])
					data.commit()
					text = "You entered the trade zone"
				else:
					text = "You're still in the trade zone"
				data.close()
				itz = True

	if not itz:
		data = sqlite3.connect('lop.db')
		c = data.cursor()
		c.execute("SELECT inTradeZone FROM players WHERE id=?", [plid])
		if int(c.fetchone()[0]) == 1:
			text = "You left the trade zone"
			c.execute("UPDATE players SET inTradeZone=0 WHERE id=?", [plid])
			data.commit()
		data.close()

	if not text:
		if random.randint(1, 100) >= 75:
			ev = random.randint(1, 3)
			if ev == 1:
				text += f"\n{events.createEvent(plid)}"
			if ev == 2:
				text += f"\n{events.genChest(plid)}"
			if ev == 3:
				text += f"\n{events.spawnMerchant(plid)}"
		else:
			text = "There's nothing here"
	return text

if __name__ == '__main__':
	pass
