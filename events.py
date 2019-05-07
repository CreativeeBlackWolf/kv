import commands as com
import xml.etree.cElementTree as ET
import random

events = ['test']

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

def event_Test():
	return "пiпався"

