import xml.etree.cElementTree as ET
import os
from colorama import init, Fore, Back, Style

def mapCreate():
	init(convert=True)
	width = height = isinf = 0
	print(Fore.LIGHTYELLOW_EX + "Размеры карты (w;h/inf): ")
	a = input()
	if not a:
		return
	if a.lower() in ["infinite", "inf"]:
		isinf = 1
	else:
		try:
			if ";" not in a:
				raise ValueError
			width = int(a.split(";")[0])
			height = int(a.split(";")[1])
		except ValueError:
			return Fore.LIGHTRED_EX + "Неверно введены размеры карты"
	layers = ["Players", "Merchants", "Chests", "Triggers", "TradeZones"]
	map = ET.Element("map", {"version": "1.2", "tiledversion": "124", "orientation": "orthogonal", 
	"renderorder": "right-down", "width": str(width), "height": str(height), "infinite": str(isinf),
	"tilewidth": "1", "tileheight": "1", "nextlayerid": str(len(layers)+1), "nextobjectid": "1"})
	for i in range(len(layers)):
		ET.SubElement(map, "objectgroup", {"id": str(i+1), "name": layers[i]})
		print(Fore.LIGHTMAGENTA_EX + f"Слой {layers[i]} создан")
	tree = ET.ElementTree(map)
	with open("session.tmx", "w"):
		tree.write("session.tmx", "UTF-8")
	return Fore.LIGHTGREEN_EX + "Файл карты успешно создан"

if __name__ == '__main__':
	print(mapCreate())
