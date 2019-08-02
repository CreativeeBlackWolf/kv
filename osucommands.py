import osulib
import osu.calc as oss
import sqlite3
import utils as ut
import os
import requests
import json
import urllib.request
from datetime import datetime
from lxml import html, etree
from PIL import Image

with open("osutoken.txt", "r") as f:
	t = f.read().split(", ")

osu = osulib.osu(t[0])
till = osulib.tillerino(t[1])

def getLength(bmid):
	return till.getBeatmapLength(bmid)

def register(uid, osuid):
	if ut.osuIsExist(uid):
		return 'Use "o!change" to change your osu! profile'
	data = sqlite3.connect("osuplayers.db")
	c = data.cursor()
	user = None
	try:
		osuid = int(osuid)
		user = osu.getUser(osuid, isID=True)
	except ValueError:
		user = osu.getUser(osuid)
	if not user:
		return "You entered wrong ID (recommended) or Username"
	c.execute("INSERT INTO players (vkid, osuid, osuname) VALUES (?, ?, ?)", [uid, user["id"], user["username"]])
	data.commit()
	data.close()
	return "Successfully registered"

def change(uid, osuid):
	if not ut.osuIsExist(uid):
		return 'Use "o!register" to register your osu! profile'
	data = sqlite3.connect("osuplayers.db")
	c = data.cursor()
	user = None
	try:
		osuid = int(osuid)
		user = osu.getUser(osuid, isID=True)
	except ValueError:
		user = osu.getUser(osuid)
	if not user:
		return "You entered wrong ID (recommended) or Username"
	c.execute("UPDATE players SET osuid=?, osuname=? WHERE vkid=?", [user["id"], user["username"], uid])
	data.commit()
	data.close()
	return "Successfully changed"

class commands():
	def __init__(self, uid):
		self.user = uid
		data = sqlite3.connect("osuplayers.db")
		c = data.cursor()
		c.execute("SELECT * FROM players WHERE vkid=?", [uid])
		self.osuid = None
		self.osuname = None
		tmp = c.fetchone()
		if tmp:
			self.osuid = tmp[1]
			self.osuname = tmp[2]
		data.close()

	def changeAvatar(self):
		if not self.osuid:
			return "Use o!register to use this command"
		r =	requests.get(f"https://osu.ppy.sh/users/{self.osuid}")
		tree = html.fromstring(r.text)
		parse = tree.xpath('//script[@id="json-user"]')[0]
		j = json.loads(parse.text)
		avatar = j["avatar_url"]
		avpath = f'avatars\\{self.osuid}.{avatar.split("/")[-1].split(".")[-1]}'
		if avatar != "/images/layout/avatar-guest.png":
			urllib.request.urlretrieve(avatar, avpath)
		else:
			urllib.request.urlretrieve(f"{osu.naurl}{avatar}", avpath)
		i = Image.open(avpath)
		if i.size == (256, 255) or i.size == (256, 256):
			country = j["country"]["code"]
			if not os.path.exists(f"countries\\{country}.png"):
				urllib.request.urlretrieve(f"https://osu.ppy.sh/images/flags/{country}.png", f"countries\\{country}.png")
			c = Image.open(f"countries\\{country}.png").convert("RGBA")
			i.paste(c, (98, 207), c)
			i.save(avpath)
			return "New avatar saved"
		return "New avatar saved, but without flag because of image size"

	def me(self):
		if not self.osuid:
			return "Use o!register to use this command"
		r =	requests.get(f"https://osu.ppy.sh/users/{self.osuid}")
		tree = html.fromstring(r.text)
		parse = tree.xpath('//script[@id="json-user"]')[0]
		j = json.loads(parse.text)
		avatar = j["avatar_url"]
		avpath = f'avatars\\{self.osuid}.{avatar.split("/")[-1].split(".")[-1]}'
		if not os.path.exists(avpath):
			if avatar != "/images/layout/avatar-guest.png":
				urllib.request.urlretrieve(avatar, avpath)
			else:
				urllib.request.urlretrieve(f"{osu.naurl}{avatar}", avpath)
			i = Image.open(avpath)
			if i.size == (256, 255) or i.size == (256, 256):
				country = j["country"]["code"]
				if not os.path.exists(f"countries\\{country}.png"):
					urllib.request.urlretrieve(f"https://osu.ppy.sh/images/flags/{country}.png", f"countries\\{country}.png")
				c = Image.open(f"countries\\{country}.png").convert("RGBA")
				i.paste(c, (98, 207), c)
				i.save(avpath)
		user = osu.getUser(self.osuid, isID=True)
		user["avatarPath"] = avpath
		return user

	def calcOppai(self, bmlink, mods = None, acc = 0.0):
		ch = requests.get(bmlink, allow_redirects=True)
		map = None
		if ch.url.split("/")[-2] in ["beatmapsets", "b"]:
			map = osu.getBeatmap(ch.url.split("/")[-1], True)
		else:
			map = osu.getBeatmap(ch.url.split("/")[-1])
		r = requests.get(ch.url)
		tree = html.fromstring(r.text)
		parse = tree.xpath('//script[@id="json-beatmapset"]')[0]
		thumbnail = json.loads(parse.text)['covers']['cover@2x']
		if not os.path.exists(f"tmpthumbs\\{map['beatmapsetid']}.jpg"):
			urllib.request.urlretrieve(thumbnail, f"tmpthumbs\\{map['beatmapsetid']}.jpg")
		bmid = map["beatmapid"]
		file = till.getBeatmapFile(bmid)
		if not file:
			return None
		with open("temp.osu", "w", encoding="utf_8_sig", newline="") as f:
			f.write(file)
		x = oss.calcMapNoDownload("temp.osu", amods=mods, acc=acc)
		x["beatmapsetid"] = map['beatmapsetid']
		return x

	def checkStatus(self, bmlink):
		ch = requests.get(bmlink, allow_redirects=True)
		map = None
		if ch.url.split("/")[-2] in ["beatmapsets", "b"]:
			map = osu.getBeatmap(ch.url.split("/")[-1], True)
		else:
			map = osu.getBeatmap(ch.url.split("/")[-1])
		try:
			if int(map["status"]) == 1:
				return True
			else:
				return False
		except TypeError:
			return False

	def calcTillerino(self, bmlink, mods=osulib.mods.NoMod.value, acc=None):
		ch = requests.get(bmlink, allow_redirects=True)
		map = None
		if ch.url.split("/")[-2] in ["beatmapsets", "b"]:
			map = osu.getBeatmap(ch.url.split("/")[-1], True)
		else:
			map = osu.getBeatmap(ch.url.split("/")[-1])
		bmid = map["beatmapid"]
		mpp = None
		if not acc:
			mpp = till.beatmapPP(bmid, m=mods)
		else:
			mpp = till.beatmapPP(bmid, m=mods, acc=acc)
		if mpp is None:
			return False
		r = requests.get(ch.url)
		tree = html.fromstring(r.text)
		parse = tree.xpath('//script[@id="json-beatmapset"]')[0]
		thumbnail = json.loads(parse.text)['covers']['cover@2x']
		if not os.path.exists(f"tmpthumbs\\{map['beatmapsetid']}.jpg"):
			urllib.request.urlretrieve(thumbnail, f"tmpthumbs\\{map['beatmapsetid']}.jpg")
		if mods == osulib.mods.NoMod.value:
			mods = "NoMod"
		else:
			mods = mods.upper()
		return dict(beatmapid=map["beatmapid"], PP=[x["pp"] for x in mpp], maxcombo=map["maxcombo"], combo=map["maxcombo"],
					AR=map["AR"], OD=map["OD"], CS=map["CS"], stars=round(float(map["stars"]), 2), beatmapsetid=map["beatmapsetid"],
					title=f"{map['artist']} - {map['title']} [{map['difficulty']}] ({mods})", acc=acc)

	def recentScore(self, user=None, mode=osulib.osuSTD):
		if not user:
			user = self.osuid
		if user:
			rs = osu.getRecent(user, mode)
			if not rs:
				return "This user has no recent scores", None
			date = datetime.strptime(rs["date"], "%Y-%m-%d %H:%M:%S")
			ch = requests.get(f"{osu.naurl}/b/{rs['bmid']}", allow_redirects=True)
			r = requests.get(ch.url)
			tree = html.fromstring(r.text)
			parse = tree.xpath('//script[@id="json-beatmapset"]')[0]
			thumbnail = json.loads(parse.text)['covers']['cover@2x']
			if not os.path.exists(f"tmpthumbs\\{rs['bmid']}.jpg"):
				urllib.request.urlretrieve(thumbnail, f"tmpthumbs\\{rs['bmid']}.jpg")
			msg = f"""Map: {rs["title"]}
Rank: {rs["rank"]} | Mods: {rs["mods"]}
300/100/50/miss: {rs["x300"]}/{rs["x100"]}/{rs["x50"]}/{rs["misses"]}
Accuracy: {rs["acc"]}%
Combo: {rs["combo"]}/{rs["maxcombo"]}
PP: {rs["pp"]}
Date: {ut.numWithZero(date.day)}-{ut.numWithZero(date.month)}-{date.year} {date.hour}:{ut.numWithZero(date.minute)}:{ut.numWithZero(date.second)}"""
			return msg, rs["bmid"]
		return "You haven't registered yet. Enter o!register to do it.", None
	
if __name__ == "__main__":
	pass
