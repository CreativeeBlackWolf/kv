import xml.etree.cElementTree as ET
import commands as com

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
	#tr = eventTrigger(plid)
	return f"You moved {direction}"

if __name__ == '__main__':
	print(move(409541670, "left"))