import xml.etree.cElementTree as ET
import sqlite3
from utils import *
import os

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
	c.execute("""
				CREATE TABLE player (
				x_pos INTEGER,
				y_pos INTEGER)""")
	c.execute("INSERT INTO player VALUES (25, 25)")
	player.commit()
	player.close()
	return f"Welcome to the gAmE, {fname}"

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

def playertomap(plid):
	pos = getCoords(plid)
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == 'Players':
			ET.SubElement(i, 'object', {'id': str(plid), 'name': str(plid), 'x': str(pos[0]), 'y': str(pos[1]), 'width': '1', 'height': '1'})
	objects = root.findall('objectgroup/object')
	for i in objects:
		print(i.attrib)
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

