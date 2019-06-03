import json
import os
import sqlite3
import random

class Item:
    def __init__(self, plid):
        self.Item = json.load(open("itemsdata.json"))
        self.plid = plid

    def addItem(self):
        item = self.Item["items"][random.randint(0, len(self.Item["items"]) - 1)]
        data = sqlite3.connect(os.path.join("pl", f"{self.plid}.db"))
        c = data.cursor()
        delete = 1 if item["delete"] else 0
        toins = [item["name"], item["desc"], item["type"], item["tier"], ", ".join(item["actions"]), delete]
        c.execute("INSERT INTO inventory (name, desc, type, tier, actions, del) VALUES(?, ?, ?, ?, ?, ?)", toins)
        data.commit()
        data.close()
        return f"You just got {item['name']}!"

if __name__ == '__main__':
    item = Item(409541670)
    item.addItem()