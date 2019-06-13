import json
import os
import sqlite3
import random
from math import ceil

class Item:
	def __init__(self, plid):
		self.Item = json.load(open("itemsdata.json"))
		self.tierList = ["Common", "Uncommon", "Rare", "Exclusive", "Absolute"]
		self.tierPrice = {"Common": 1, "Uncommon": 1.2, "Rare": 1.5, "Exclusive": 2, "Absolute": 3}
		self.plid = plid

	def addItem(self, *tiers):
		if not tiers:
			randtier = random.choice(self.tierList)
		else:
			randtier = random.choice(tiers)
		item = self.Item["items"][randtier][random.randint(0, len(self.Item["items"][randtier])-1)]
		data = sqlite3.connect(os.path.join("pl", f"{self.plid}.db"))
		c = data.cursor()
		delete = 1 if item["delete"] else 0
		toins = [item["name"], item["desc"], item["type"], item["tier"], " | ".join(item["actions"]), delete]
		c.execute("INSERT INTO inventory (name, desc, type, tier, actions, del, inTrade) VALUES(?, ?, ?, ?, ?, ?, 0)", toins)
		data.commit()
		data.close()
		return f"You just got {item['name']}!"

	def addMerchantItem(self, coords, *tiers):
		if not tiers:
			randtier = random.choice(self.tierList[0:3])
		else:
			randtier = random.choice(tiers)
		item = self.Item["items"][randtier][random.randint(0, len(self.Item["items"][randtier])-1)]
		print(item)
		merch = sqlite3.connect(os.path.join("npc", f"merchant-{coords[0]}{coords[1]}.db"))
		c = merch.cursor()
		delete = 1 if item["delete"] else 0
		price = random.randint(len(item['actions'])+10, ceil(len(item['actions'])+18*self.tierPrice[randtier]))
		toins = [item["name"], item["desc"], item["type"], item["tier"], " | ".join(item["actions"]), delete, price]
		c.execute("INSERT INTO inventory (name, desc, type, tier, actions, del, price) VALUES(?, ?, ?, ?, ?, ?, ?)", toins)
		merch.commit()
		merch.close()

	def test(self):
		pass

if __name__ == '__main__':
	item = Item(409541670)
	print(item.addMerchantItem())