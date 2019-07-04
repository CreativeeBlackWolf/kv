import xml.etree.cElementTree as ET
import sqlite3
import vk_api
from utils import *
import versions
import os
import random
from math import ceil
import events as ev

with open('token.txt', 'r') as f:
	token = f.read()
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

rulesofinternet = {
	'1': "Do not talk about /b/",
	'2': "Do NOT talk about /b/",
	'3': "We are Anonymous",
	'4': "Anonymous is legion",
	'5': "Anonymous never forgives",
	'6': "Anonymous can be a horrible, senseless, uncaring monster",
	'7': "Anonymous is still able to deliver",
	'8': "There are no real rules about posting",
	'9': "There are no real rules about moderation either - enjoy your ban",
	'10': "If you enjoy any rival sites - DON'T",
	'11': "All your carefully picked arguments can easily be ignored",
	'12': "Anything you say can and will be used against you",
	'13': "Anything you say can be turned into something else - fixed",
	'14': "Do not argue with trolls - it means that they win",
	'15': "The harder you try the harder you will fail",
	'16': "If you fail in epic proportions, it may just become a winning failure",
	'17': "Every win fails eventually",
	'18': "Everything that can be labeled can be hated",
	'19': "The more you hate it the stronger it gets",
	'20': "Nothing is to be taken seriously",
	'21': "Original content is original only for a few seconds before getting old",
	'22': "Copypasta is made to ruin every last bit of originality",
	'23': "Copypasta is made to ruin every last bit of originality",
	'24': "Every repost is always a repost of a repost",
	'25': "Relation to the original topic decreases with every single post",
	'26': "Any topic can be easily turned into something totally unrelated",
	'27': "Always question a person's sexual preferences without any real reason",
	'28': "Always question a person's gender - just in case it's really a man",
	'29': "In the internet all girls are men and all kids are undercover FBI agents",
	'30': "There are no girls on the internet",
	'31': "TITS or GTFO - the choice is yours",
	'32': "You must have pictures to prove your statements",
	'33': "Lurk more - it's never enough",
	'34': "There is porn of it, no exceptions",
	'35': "If no porn is found at the moment, it will be made",
	'36': "There will always be even more fucked up shit than what you just saw",
	'37': "You cannot divide by zero (just because the calculator says so)",
	'38': "No real limits of any kind apply here - not even the sky",
	'39': "CAPSLOCK IS CRUISE CONTROL FOR COOL",
	'40': "EVEN WITH CRUISE CONTROL YOU STILL HAVE TO STEER",
	'41': "Desu isn't funny. Seriously guys. It's worse than Chuck Norris jokes.",
	'42': "Nothing is Sacred",
	'43': "The more beautiful and pure a thing is - the more satisfying it is to corrupt it",
	'44': "Even one positive comment about Japanese things can make you a weeaboo",
	'45': "When one sees a lion, one must get into the car",
	'46': "There is always furry porn of it",
	'47': "The pool is always closed",
	'48': "?????",
	'49': "PROFIT!",
}

class stats:
	def __init__(self, plid):
		data = sqlite3.connect(os.path.join('pl', '{}.db'.format(plid)))
		c = data.cursor()
		c.execute("SELECT x_pos FROM player")
		self.x_pos = int("{[0]}".format(c.fetchone()))
		c.execute("SELECT y_pos FROM player")
		self.y_pos = int("{[0]}".format(c.fetchone()))
		c.execute("SELECT money FROM player")
		self.money = int("{[0]}".format(c.fetchone()))


def rofi(num):
	if num in rulesofinternet:
		return "{}: {}".format(num, rulesofinternet[str(num)])
	else:
		return "Index is out of range (total rules in the database: {})".format(len(rulesofinternet))

def register(plid, fname, lname):
	if isExist(plid):
		return "U're already registered"
	
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("INSERT INTO players VALUES (?, ?, ?)", [plid, f"{fname} {lname}", versions.latestVersion])
	data.commit()
	data.close()

	player = sqlite3.connect(os.path.join('pl', '{}.db'.format(plid)))
	c = player.cursor()
	c.execute("CREATE TABLE player (x_pos INTEGER, y_pos INTEGER, money INTEGER)")
	c.execute("INSERT INTO player VALUES (25, 25, 127, 0)")
	c.execute("CREATE TABLE friends (id INTEGER, name TEXT, status INTEGER)")
	c.execute("""CREATE TABLE inventory (number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL,
					desc TEXT NOT NULL,
					type TEXT NOT NULL,
					tier TEXT NOT NULL,
					actions TEXT NOT NULL,
					del BOOLEAN NOT NULL,
					inTrade BOOLEAN)""")
	c.execute("""CREATE TABLE trades (tradeNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					tradeType TEXT NOT NULL,
					tradeDesc TEXT NOT NULL,
					tradeStatus TEXT NOT NULL,
					name TEXT NOT NULL,
					desc TEXT NOT NULL,
					type TEXT NOT NULL,
					tier TEXT NOT NULL,
					actions TEXT NOT NULL,
					del BOOLEAN NOT NULL,
					senderID TEXT NOT NULL,
					oiNum INTEGER NOT NULL)""")
	player.commit()
	player.close()
	return f"Welcome to the game, {fname}"

def delete(plid):
	if not isExist(plid):
		return "Register first"
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("DELETE FROM players WHERE id=?", [plid])
	data.commit()
	data.close()
	try:
		os.remove(os.path.join("pl", f"{plid}.db"))
	except FileNotFoundError:
		print(f"db not found while deleting {plid}")
	return "Account deleted. Seeya next time"

def addFriend(plid, fid):
	if not isExist(plid):
		return "Register first"
	if not isExist(fid):
		return "ID is not registered"
	if str(plid) == str(fid):
		return "You have no friends?"
	player = sqlite3.connect(os.path.join('pl', f'{plid}.db'))
	c = player.cursor()
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	answer = c.fetchone()
	if answer is None:
		c.execute("INSERT INTO friends VALUES (?, ?, ?)", [fid, searchByID(fid), "Requested"])
		player.commit()
		player.close()
		friend = sqlite3.connect(os.path.join("pl", f"{fid}.db"))
		c = friend.cursor()
		c.execute("INSERT INTO friends VALUES (?, ?, ?)", [plid, searchByID(plid), "Request"])
		vk.messages.send(user_id=fid, message=f"""{searchByID(plid)} sent a friend request.
Enter "/addfriend {plid}" to accept it.
Enter "/denyrequest {plid}" to deny it.""")
		friend.commit()
		friend.close()
		return "Request sent"
	if answer[2] == "Requested":
		return "Request already sended"
	if answer[2] == "Request":
		c.execute("UPDATE friends SET status='Accepted' WHERE id=?", [fid])
		player.commit()
		player.close()
		friend = sqlite3.connect(os.path.join("pl", f"{fid}.db"))
		c = friend.cursor()
		c.execute("UPDATE friends SET status='Accepted' WHERE id=?", [plid])
		vk.messages.send(user_id=fid, message=f"{searchByID(plid)} has accepted friend request")
		friend.commit()
		friend.close()
		return "Request accepted"

def showInventory(plid):
	if not isExist(plid):
		return "Register first"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM inventory ORDER BY number")
	items = c.fetchall()
	if not items:
		return "You have no items in inventory"
	message = ""
	for i in items:
		message += f"{i[0]}. {i[1]} // {i[2]}\n"
	return message

def showTradeInventory(plid):
	if not isExist(plid):
		return "Register first"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM trades ORDER BY tradeNumber")
	trades = c.fetchall()
	if not trades:
		return "You have no trades"
	msg = ""
	for i in trades:
		msg += f"{i[0]}. Type: {i[1]}, Status: {i[3]}\nItem: {i[4]}\nDescription: {i[2]}\n\n"
	return msg

def sendMoney(plid, fid, count):
	if not isExist(plid):
		return "Register first"
	if not isExist(fid):
		return "User is not found"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	st = stats(plid)
	if st.money < int(count):
		return "Not enough money to send"
	c.execute("UPDATE player SET money = money - ?", [count])
	data.commit()
	data.close()
	pl = sqlite3.connect(os.path.join("pl", f"{fid}.db"))
	c = pl.cursor()
	c.execute("UPDATE player SET money = money + ?", [count])
	pl.commit()
	pl.close()
	sender = vk.users.get(user_ids=plid, name_case="gen")[0]
	vk.messages.send(user_id=fid, message=f"You got {count} credits from {sender['first_name']} {sender['last_name']}")
	return "Your money were successfully sent to the player"

def sendGift(plid, fid, itemNumber, message):
	if not isExist(fid):
		return "User is not found"
	if not inFriends(plid, fid):
		return "User isn't in your friend list"
	if not inInventory(plid, itemNumber):
		return "Item is not found"
	if inTrade(plid, itemNumber):
		return "This item is already in trade"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM inventory WHERE number=?", [itemNumber])
	sItem = c.fetchone()
	message = f"{' '.join(message)}"
	sender = vk.users.get(user_ids=plid, name_case="gen")[0]
	receiver = vk.users.get(user_ids=fid, name_case="dat")[0]
	c.execute("""INSERT INTO trades (tradeType, tradeDesc, tradeStatus, name, desc, type, tier, actions, del, senderID, oiNum)
				VALUES ("Gift", ?, "Sended", ?, ?, ?, ?, ?, ?, ?, ?)""", [f"Gift to {receiver['first_name']} {receiver['last_name']}: {message}",
				sItem[1], sItem[2], sItem[3], sItem[4], sItem[5], sItem[6], plid, itemNumber])
	c.execute("UPDATE inventory SET inTrade=1 WHERE number=?", [itemNumber])
	data.commit()
	data.close()
	fdata = sqlite3.connect(os.path.join("pl", f"{fid}.db"))
	c = fdata.cursor()
	c.execute("""INSERT INTO trades (tradeType, tradeDesc, tradeStatus, name, desc, type, tier, actions, del, senderID, oiNum)
				VALUES ("Gift", ?, "Awaiting", ?, ?, ?, ?, ?, ?, ?, ?)""", [f"Gift from {sender['first_name']} {sender['last_name']}: {message}",
				sItem[1], sItem[2], sItem[3], sItem[4], sItem[5], sItem[6], plid, itemNumber])
	c.execute("SELECT tradeNumber FROM trades ORDER BY tradeNumber DESC LIMIT 1")
	tradeNum = c.fetchone()[0]
	fdata.commit()
	fdata.close()
	vk.messages.send(user_id=fid, message=f"""You got a Gift from {sender['first_name']} {sender['last_name']} with message: {message}
Enter /acceptGift {tradeNum} to accept it
Or enter /rejectGift {tradeNum} to reject it""")
	return "Trade request sended."

def acceptGift(plid, tradeNumber):
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM trades WHERE tradeNumber=?", [tradeNumber])
	item = c.fetchone()
	if item is None:
		return "Trade request isn't found"
	c.execute("INSERT INTO inventory (name, desc, type, tier, actions, del, inTrade) VALUES (?, ?, ?, ?, ?, ?, 0)", [item[4], item[5], item[6], item[7], item[8], item[9]])
	c.execute("UPDATE trades SET tradeStatus='Accepted' WHERE tradeNumber=?", [tradeNumber])
	data.commit()
	data.close()
	fdata = sqlite3.connect(os.path.join("pl", f"{item[10]}.db"))
	c = fdata.cursor()
	c.execute("DELETE FROM inventory WHERE number=?", [item[11]])
	c.execute("UPDATE trades SET tradeStatus='Accepted' WHERE oiNum=?", [item[11]])
	c.execute("SELECT tradeNumber FROM trades WHERE oiNum=?", [item[11]])
	tr = c.fetchone()[0]
	fdata.commit()
	fdata.close()
	vk.messages.send(user_id=item[10], message=f"Your gift (trade№: {tr}) was accepted")
	return "Gift accepted and added to your inventory"

def rejectGift(plid, tradeNumber):
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM trades WHERE tradeNumber=?", [tradeNumber])
	tr = c.fetchone()
	if tr is None:
		return "Trade request isn't found"
	c.execute("UPDATE trades SET tradeStatus='Rejected' WHERE tradeNumber=?", [tradeNumber])
	data.commit()
	data.close()
	fdata = sqlite3.connect(os.path.join("pl", f"{tr[10]}.db"))
	c = fdata.cursor()
	c.execute("UPDATE trades SET tradeStatus='Rejected' WHERE oiNum=?", [tr[11]])
	c.execute("UPDATE inventory SET inTrade=0 WHERE number=?", [tr[11]])
	c.execute("SELECT tradeNumber FROM trades WHERE oiNum=?", [tr[11]])
	tr = c.fetchone()[0]
	fdata.commit()
	fdata.close()
	vk.messages.send(user_id=tr[10], message=f"Your gift (trade№: {tr}) was accepted")
	return "Gift rejected"

def showShopList(plid):
	coords = getCoords(plid)
	x = coords[0]
	y = coords[1]
	if not os.path.exists(os.path.join("npc", f"merchant-{x}{y}.db" )):
		return "Here's no merchant on this square"
	data = sqlite3.connect(os.path.join("npc", f"merchant-{x}{y}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM inventory")
	if c.fetchone() is None:
		if ev.refillMerchant is False:
			if random.randint() <= 50:
				return ev.removeMerchant(plid)
			else:
				return "Merchant doesn't have any items now. Check him later"
		else:
			return "Merchant just got new items! Reenter the command to check them"
	c.execute("SELECT * FROM inventory")
	it = c.fetchall()
	msg = "Merchant shop list:\n"
	for i in it:
		msg += f"{i[0]}. {i[1]} // Price: {i[7]}\n"
	data.close()
	return msg

def itemDesc(plid, itemNumber):
	if not isExist(plid):
		return "User is not found"
	if not inInventory(plid, itemNumber):
		return "Item is not found"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT name, desc FROM inventory WHERE number=?", [itemNumber])
	desc = c.fetchone()
	data.close()
	return f"{desc[0]} ({desc[1]})"

def buyItem(plid, itemNumber):
	coords = getCoords(plid)
	x = coords[0]
	y = coords[1]
	if not os.path.exists(os.path.join("npc", f"merchant-{x}{y}.db" )):
		return "Here's no merchant on this square"
	st = stats(plid)
	data = sqlite3.connect(os.path.join("npc", f"merchant-{x}{y}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM inventory")
	c.execute("SELECT price FROM inventory WHERE number=?", [itemNumber])
	if c.fetchone() is None:
		return "Wrong item number"
	c.execute("SELECT price FROM inventory WHERE number=?", [itemNumber])
	price = int(c.fetchone()[0])
	if st.money < price:
		return "You can't buy this item"
	c.execute("SELECT * FROM inventory WHERE number=?", [itemNumber])
	item = c.fetchone()
	c.execute("DELETE FROM inventory WHERE number=?", [itemNumber])
	pldata = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = pldata.cursor()
	c.execute("INSERT INTO inventory (name, desc, type, tier, actions, del, inTrade) VALUES (?, ?, ?, ?, ?, ?, 0)",
				[item[1], item[2], item[3], item[4], item[5], item[6]])
	c.execute("""INSERT INTO trades (tradeType, tradeDesc, tradeStatus, name, desc, type, tier, actions, del, senderID, oiNum)
				VALUES ("Purchase", ?, "Done", ?, ?, ?, ?, ?, ?, ?, ?)""",
				[f"Purchase for {price} riphs", item[1], item[2], item[3], item[4], item[5], item[6], f"merchant-{x}{y}", item[0]])
	data.commit()
	data.close()
	pldata.commit()
	pldata.close()
	return "Item bought"

def sellItem(plid, itemNumber):
	coords = getCoords(plid)
	x = coords[0]
	y = coords[1]
	if not os.path.exists(os.path.join("npc", f"merchant-{x}{y}.db")):
		return "Here's no merchant on this square"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	if not inInventory(plid, itemNumber):
		return "Wrong item number"
	c.execute("SELECT * FROM inventory WHERE number=?", [itemNumber])
	item = c.fetchone()
	if item[4] == "Common":
		mp = 1
	if item[4] == "Uncommon":
		mp = 1.2
	if item[4] == "Rare":
		mp = 1.4
	if item[4] == "Exclusive":
		mp = 1.8
	if item[4] == "Absolute":
		mp = 2.2
	actions = item[5].split(" | ")
	mdata = sqlite3.connect(os.path.join("npc", f"merchant-{x}{y}.db"))
	mc = mdata.cursor()
	mc.execute("SELECT * FROM spList WHERE name=?", [item[1]])
	if mc.fetchone() is None:
		price = random.randint(len(actions)+8, ceil(len(actions)+10*mp))
		mc.execute("INSERT INTO spList VALUES(?, ?)", [item[2], price])
		mdata.commit()
	else:
		mc.execute("SELECT price FROM spList WHERE name=?", [item[2]])
		price = int(mc.fetchone()[0])
	mdata.close()
	c.execute("DELETE FROM inventory WHERE itemNumber=?", [itemNumber])
	c.execute("UPDATE player SET money = money + ?", [price])
	c.execute(f"""INSERT INTO trades (tradeType, tradeDesc, tradeStatus, name, desc, type, tier, actions, del, senderID, oiNum)
				VALUES ('Sale', ?, 'Done', ?, ?, ?, ?, ?, ?, ?, ?)""",
				[f"Selling item for {price}", item[1], item[2], item[3], item[4], item[5], item[6], f"merchant-{x}{y}", itemNumber])
	data.commit()
	data.close()
	return f"Item sold, you got {price}"

def putUpForAuc(plid, itemNumber, price):
	if not inInventory(plid, itemNumber):
		return "Wrong item number"
	if not inTradeZone(plid):
		return "You must be in trade zone to put the item up"
	if inTrade(plid, itemNumber):
		return "This item is already in some trade"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("UPDATE inventory SET inTrade=1 WHERE number=?", [itemNumber])

def removeFriend(plid, fid):
	if not isExist(plid):
		return "Register first"
	if not isExist(fid) and str(fid) != "???":
		return "User is not found"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	if c.fetchone() is None:
		return "User is not in your friends list"
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	ans = c.fetchone()
	if ans[2] == "Accepted":
		c.execute("SELECT name FROM friends WHERE id=?", [fid])
		if c.fetchone()[0] == "Cassette":
			return "You can't remove this cute thing from friend list"
		c.execute("DELETE FROM friends WHERE id=?", [fid])
		data.commit()
		data.close()
		friend = sqlite3.connect(os.path.join("pl", f"{fid}.db"))
		c = friend.cursor()
		c.execute("DELETE FROM friends WHERE id=?", [plid])
		vk.messages.send(user_id=fid, message=f"{searchByID(plid)} has removed you from friend list. :c\nUse \"/addfriend {plid}\" to send friend request")
		friend.commit()
		friend.close()
		return f"User has been removed from your friend list. \nUse \"/addfriend {fid}\" to send friend request"
	else:
		return "Please, use \"/denyrequest\" to cancel or deny friend request."

def denyFriendRequest(plid, fid):
	if not isExist(plid):
		return "Register first"
	data = sqlite3.connect(os.path.join('pl', f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	answer = c.fetchone()
	if answer is None:
		return "This user isn't sent a request"
	if answer[2] == "Request":
		c.execute("DELETE FROM friends WHERE id=?", [fid])
		data.commit()
		data.close()
		friend = sqlite3.connect(os.path.join("pl", f"{fid}.db"))
		c = friend.cursor()
		c.execute("DELETE FROM friends WHERE id=?", [plid])
		vk.messages.send(user_id=fid, message=f"{searchByID(plid)} has denied friend request")
		friend.commit()
		friend.close()
		return "Request denied"
	if answer[2] == "Requested":
		c.execute("DELETE FROM friends WHERE id=?", [fid])
		data.commit()
		data.close()
		friend = sqlite3.connect(os.path.join("pl", f"{fid}.db"))
		c = friend.cursor()
		c.execute("DELETE FROM friends WHERE id=?", [plid])
		vk.messages.send(user_id=fid, message=f"{searchByID(plid)} has canceled friend request")
		friend.commit()
		friend.close()
		return "Request canceled"
	if answer[2] == "Accepted":
		return "Request already accepted."

def friendList(plid):
	if not isExist(plid):
		return "Register first"
	data = sqlite3.connect(os.path.join('pl', f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM friends WHERE status='Accepted'")
	message = "Mutual friends:"
	if c.fetchone() is None:
		message += "\nYou don't have any friends ;c"
	else:
		c.execute("SELECT * FROM friends WHERE status='Accepted'")
		friends = c.fetchall()
		for f in friends:
			message += f"\n{f[1]} ({f[0]})"
	c.execute("SELECT * FROM friends WHERE status='Requested'")
	message += "\n\nPending acceptance/rejection:"
	if c.fetchone() is None:
		message += "\nNo requests sent"
	else:
		c.execute("SELECT * FROM friends WHERE status='Requested'")
		awaiting = c.fetchall()
		for a in awaiting:
			message += f"\n{a[1]} ({a[0]})"
	c.execute("SELECT * FROM friends WHERE status='Request'")
	message += "\n\nPending for reply:"
	if c.fetchone() is None:
		message += "\nNo requests sent"
	else:
		c.execute("SELECT * FROM friends WHERE status='Request'")
		repl = c.fetchall()
		for r in repl:
			message += f"\n{r[1]} ({r[0]})"
	return message

def searchByID(id):
	if not isExist(id):
		return "User is not found"
	data = sqlite3.connect("lop.db")
	c = data.cursor()
	c.execute("SELECT name FROM players WHERE id=?", [id])
	name = c.fetchone()
	data.close()
	return name[0]

def playersOnTile(plid):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	pos = getCoords(plid)
	x = int(pos[0])
	y = int(pos[1])
	tileplayers = []
	
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == "Players":
			for players in i:
				if int(players.attrib['x']) == x and int(players.attrib['y']) == y:
					tileplayers.append(players.attrib['name'])
	
	if not tileplayers:
		return "There's no players on tile"
	else:
		message = "Players on tile:"
		for i in tileplayers:
			message = message + f"\n{searchByID(i)}"
		return message

def save(plid):
	data = sqlite3.connect(os.path.join('pl', f"{plid}.db"))
	c = data.cursor()
	pos = getCoords(plid)
	c.execute("UPDATE player SET x_pos=?, y_pos=?", [pos[0], pos[1]])
	data.commit()
	data.close()
	return "Position saved."

def playerToMap(plid):
	pos = getCoords(plid)
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == 'Players':
			ET.SubElement(i, 'object', {'id': str(plid), 'name': str(plid), 'type': 'Player', 'x': str(pos[0]), 'y': str(pos[1]), 'width': '1', 'height': '1'})
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == 'Players':
			for p in i:
				if p.attrib['name'] == str(plid):
					ET.SubElement(p, 'ellipse')
	tree.write('session.tmx', 'UTF-8')

def mapLeave(plid):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	data = sqlite3.connect(os.path.join('pl', '{}.db'.format(plid)))
	c = data.cursor()
	position = getCoords(plid)
	c.execute("UPDATE player SET x_pos={}, y_pos={}".format(position[0], position[1]))
	data.commit()
	data.close()
	for objects in root.findall('objectgroup'):
		if objects.attrib['name'] == "Players":
			for x in objects:
				if x.attrib['name'] == str(plid):
					objects.remove(x)
					tree.write('session.tmx', 'UTF-8')

def getCoords(plid):
	if not isExist(plid):
		return "Register first"
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	for i in root.findall("objectgroup"):
		if i.attrib["name"] == "Players":
			for pos in i:
				if pos.attrib["name"] == str(plid):
					x = pos.attrib['x']
					y = pos.attrib['y']
					return x, y
	st = stats(plid)
	return st.x_pos, st.y_pos	

if __name__ == '__main__':
	pass
