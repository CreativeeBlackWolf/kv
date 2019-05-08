import xml.etree.cElementTree as ET
import commands as com
import vk_api
import events
import random

with open('token.txt', 'r') as f:
	token = f.read()
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

def move(plid, direction):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	oldcoords = com.getCoords(plid)
	for objects in root.findall('objectgroup'):
		if objects.attrib['name'] == "Players":
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
					print(f"{plid} moved: {oldcoords[0]}; {oldcoords[1]} -> {m.attrib['x']}; {m.attrib['y']}")
	tree.write('session.tmx', 'UTF-8')
	tr = eventTrigger(plid)
	return f"You moved {direction}\n\n{tr}"

def chat(plid, msg):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	pos = com.getCoords(plid)
	msg = f"{' '.join(msg)}"
	x = int(pos[0])
	y = int(pos[1])
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == "Players":
			for players in i:
				if int(players.attrib['x']) == x and int(players.attrib['y']) == y:
					vk.messages.send(user_id=players.attrib['name'], message=f"{com.searchByID(plid)}: {msg}")

def eventTrigger(plid):
	tree = ET.parse("session.tmx")
	root = tree.getroot()
	pos = com.getCoords(plid)
	x = int(pos[0])
	y = int(pos[1])
	text = ""
	for i in root.findall('objectgroup'):
		if i.attrib['name'] == "Players":
			for players in i:
				if int(players.attrib['x']) == x and int(players.attrib['y']) == y:
					if players.attrib['name'] != str(plid):
						vk.messages.send(user_id=players.attrib['name'], message=f"The {com.searchByID(plid)} has come")
						text = "There's some players on this position"

	for i in root.findall('objectgroup'):
		if i.attrib['name'] == "Triggers":
			for triggers in i:
				if int(triggers.attrib['x']) == x and int(triggers.attrib['y']) == y:
					trtype = triggers.attrib['type']
					if trtype == "test":
						i.remove(triggers)
						tree.write('session.tmx', 'UTF-8')
						text = text + f"\n{events.event_Test()}"
						break

	if not text:
		if random.randint(1, 100) >= 90:
			text = text + f"\n{events.createEvent(plid)}"
		else:
			text = "There's nothing here"
	return text

if __name__ == '__main__':
	pass
