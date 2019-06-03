import xml.etree.cElementTree as ET
import sqlite3
import vk_api
from utils import *
import os

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
	c.execute("INSERT INTO players VALUES (?, ?)", [plid, f"{fname} {lname}"])
	data.commit()
	data.close()

	player = sqlite3.connect(os.path.join('pl', '{}.db'.format(plid)))
	c = player.cursor()
	c.execute("CREATE TABLE player (x_pos INTEGER, y_pos INTEGER, money INTEGER)")
	c.execute("INSERT INTO player VALUES (25, 25, 127)")
	c.execute("CREATE TABLE friends (id INTEGER, name TEXT, status INTEGER)")
	c.execute("""CREATE TABLE inventory (number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL,
					desc TEXT NOT NULL,
					type TEXT NOT NULL,
					tier TEXT NOT NULL,
					actions TEXT NOT NULL,
					del BOOLEAN)""")
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
	if plid == fid:
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

def removeFriend(plid, fid):
	if not isExist(plid):
		return "Register first"
	if not isExist(fid):
		return "User is not found"
	data = sqlite3.connect(os.path.join("pl", f"{plid}.db"))
	c = data.cursor()
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	if c.fetchone() is None:
		return "User is not in your friends list"
	c.execute("SELECT * FROM friends WHERE id=?", [fid])
	ans = c.fetchone()
	if ans[2] == "Accepted":
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
		message = message + "\nYou don't have any friends ;c"
	else:
		c.execute("SELECT * FROM friends WHERE status='Accepted'")
		friends = c.fetchall()
		for f in friends:
			message = message + f"\n{f[1]} ({f[0]})"
	c.execute("SELECT * FROM friends WHERE status='Requested'")
	message = message + "\n\nAwaiting for answer:"
	if c.fetchone() is None:
		message = message + "\nNo requests sent"
	else:
		c.execute("SELECT * FROM friends WHERE status='Requested'")
		awaiting = c.fetchall()
		for a in awaiting:
			message = message + f"\n{a[1]} ({f[0]})"
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

def playertomap(plid):
	pos = getCoords(plid)
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == 'Players':
			ET.SubElement(i, 'object', {'id': str(plid), 'name': str(plid), 'x': str(pos[0]), 'y': str(pos[1]), 'width': '1', 'height': '1'})
	objects = root.findall('objectgroup/object')
	for i in objects:
		if i.attrib['name'] == str(plid):
			ET.SubElement(i, 'ellipse')
	tree.write('session.tmx', 'UTF-8')

def mapLeave(plid):
	'''
	Deleting players from the map
	player.mapLeave(message.author.id)
	'''
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	data = sqlite3.connect(os.path.join('pl', '{}.db'.format(plid)))
	c = data.cursor()
	position = getCoords(plid)
	c.execute("UPDATE player SET x_pos={}, y_pos={}".format(position[0], position[1]))
	data.commit()
	data.close()
	for objects in root.findall('objectgroup'):
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
	print(showInventory(409541670))
