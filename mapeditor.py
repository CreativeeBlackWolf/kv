import xml.etree.cElementTree as ET
import os
import utils

def main():
	while True:
		if not os.path.exists("session.tmx"):
			cm = input("Файл карты не был найден. Создать его? (y/n)")
			if cm in ["да", "yes", "y", "д", "пизда"]:
				createmap = utils.dynamicImport("mapManagment")
				createmap.mapCreate()
				continue
			else:
				return "Выход..."
		try:
			a = int(input("\nВыберите действие:\n1. Редактировать клетку\n2. Удалить клетку\n3. Просмотреть все объекты данного типа\n4. Убрать все объекты игроков\n5. Создать торговую зону\n6. Создать клетку\n7. Телепортировать игрока\n9. Выход\n>>>"))
		except ValueError:
			continue
		if not a:
			continue
		tree = ET.parse("session.tmx")
		root = tree.getroot()
		if a == 1:
			while True:
				coords = input("Координаты клетки (x;y): ")
				if not coords:
					break
				coords = coords.split(";")
				try:
					x = int(coords[0])
					y = int(coords[1])
				except ValueError:
					print("Неверно введены координаты")
					continue
				for objects in root.findall('objectgroup'):
					for i in objects:
						if int(i.attrib['x']) == x and int(i.attrib['y']) == y:
							edit = int(input(f"Выберите действие для {i.attrib['name']}/{i.attrib['type']}:\n1. Изменить тип объекта на схожий\n2. Изменить объект\n9. Отмена\n>>>"))
							if edit == 1:
								if objects.attrib['name'] == "Chests":
									typeEdit = int(input("Изменить тип сундука на:\n1. ClosedStandart\n2. ClosedRare\n3. ClosedExclusive\n4. ClosedAbsolute\n5. Отмена\n>>>"))
									if typeEdit == 5:
										break
									if typeEdit == 1:
										i.set("type", "ClosedStandart")
									elif typeEdit == 2:										
										i.set("type", "ClosedRare")
									elif typeEdit == 3:
										i.set("type", "ClosedExclusive")
									elif typeEdit == 4:
										i.set("type", "ClosedAbsolute")
									else:
										break
									tree.write("session.tmx", "UTF-8")
									print("Объект успешно изменён")
								if objects.attrib['name'] == "Triggers":
									typeEdit = int(input("Изменить тип триггера на:\n1. eventTest\n9. Отмена\n>>>"))
									if typeEdit == 9:
										break
									if typeEdit == 1:
										i.set("type", "test")
									else:
										break
									tree.write("session.tmx", "UTF-8")
									print("Объект успешно изменён")
								if objects.attrib['name'] == "Players":
									print("Вы не можете редактировать параметры игроков")
									break
							if edit == 2:
								if objects.attrib['name'] != "Players":
									try:
										typeEdit = int(input("Изменить объект на:\n1. Chest\n2. Event\n9. Выход\n>>>"))
									except ValueError:
										print("Неверно введён аргумент")
										break
									if typeEdit == 1:
										try:
											chestType = int(input("Тип сундука:\n1. ClosedStandart\n2. ClosedRare\n3. ClosedExclusive\n4. ClosedAbsolute\n5. Отмена\n>>>"))
										except ValueError:
											print("Неверно введён аргумент")
											break
										if chestType not in [1, 2, 3, 4, 5]:
											print("Неверно введён аргумент")
											break
										if chestType == 5:
											break
										for sc in root.findall("objectgroup"):
											if sc.attrib['name'] == "Chests":
												if chestType == 1:
													ET.SubElement(sc, 'object', {"name": "Chest", "type": "ClosedStandart", "x": str(x), "y": str(y), 'width': '1', 'height': '1'})
												elif chestType == 2:										
													ET.SubElement(sc, 'object', {"name": "Chest", "type": "ClosedRare", "x": str(x), "y": str(y), 'width': '1', 'height': '1'})
												elif chestType == 3:
													ET.SubElement(sc, 'object', {"name": "Chest", "type": "ClosedExclusive", "x": str(x), "y": str(y), 'width': '1', 'height': '1'})
												elif chestType == 4:
													ET.SubElement(sc, 'object', {"name": "Chest", "type": "ClosedAbsolute", "x": str(x), "y": str(y), 'width': '1', 'height': '1'})
												else:
													break
												objects.remove(i)
												tree.write("session.tmx", "UTF-8")
												print("Объект успешно изменён")
												break
									if typeEdit == 2:
										try:
											eventType = int(input("Тип ивента:\n1. eventTest\n9. Отмена\n>>>"))
										except ValueError:
											print("Неверно введён аргумент")
											break
										if eventType == 9:
											break
										for sc in root.findall("objectgroup"):
											if sc.attrib['name'] == "Triggers":
												if eventType == 1:
													ET.SubElement(sc, 'object', {"name": "eventTest", "type": "test", "x": str(x), "y": str(y), 'width': '1', 'height': '1'})
												else:
													break
												objects.remove(i)
												tree.write("session.tmx", "UTF-8")
												print("Объект успешно изменён")
										break
								else:
									print("Вы не можете редактировать параметры игроков")
									break
							if edit == 9:
								break
		elif a == 2:
			while True:
				coords = input("\nКоординаты клетки (x;y): ")
				if not coords:
					break
				coords = coords.split(";")
				try:
					x = int(coords[0])
					y = int(coords[1])
				except ValueError:
					print("Неверно введены координаты")
					continue
				for objects in root.findall('objectgroup'):
					if objects.attrib['name'] != "Players":
						for i in objects:
							if int(i.attrib['x']) == x and int(i.attrib['y']) == y:
								ans = input(f"Вы уверены, что хотите удалить {i.attrib['name']}//{i.attrib['type']}? ")
								if ans in ["да", "yes", "y", "д", "пизда"]:
									objects.remove(i)
									tree.write("session.tmx", "UTF-8")
									print("Объект успешно удалён")
									break
								else:
									print("Удаление отменено")
									break
		elif a == 3:
			while True:
				try:
					t = int(input("\nОбъекты:\n1. Игроки\n2. Триггеры\n3. Сундуки\n4. Торговцы\n5. Всё\n9. Выход\n>>>"))
				except ValueError:
					continue
				if t == 1:
					players = []
					for objects in root.findall('objectgroup'):
						if objects.attrib['name'] == "Players":
							for pl in enumerate(objects):
								players.append(f"{pl[0]+1}. {pl[1].attrib['name']}: {pl[1].attrib['x']};{pl[1].attrib['y']}")
					if not players:
						print("Игроков на карте не обнаружено")
					else:
						print("\n".join(players))
				if t == 2:
					triggers = []
					for objects in root.findall('objectgroup'):
						if objects.attrib['name'] == "Triggers":
							for tr in enumerate(objects):
								triggers.append(f"{tr[0]+1}. {tr[1].attrib['name']}/{tr[1].attrib['type']}: {tr[1].attrib['x']};{tr[1].attrib['y']}")
					if not triggers:
						print("Триггеров на карте не обнаружено")
					else:
						print("\n".join(triggers))
				if t == 3:
					chests = []
					for objects in root.findall('objectgroup'):
						if objects.attrib['name'] == "Chests":
							for ch in enumerate(objects):
								chests.append(f"{ch[0]+1}. {ch[1].attrib['name']}/{ch[1].attrib['type']}: {ch[1].attrib['x']};{ch[1].attrib['y']}")
					if not chests:
						print("Сундуков на карте не обнаружено")
					else:
						print("\n".join(chests))
				if t == 4:
					merchants = []
					for objects in root.findall('objectgroup'):
						if objects.attrib['name'] == "Chests":
							for mr in enumerate(objects):
								merchants.append(f"{mr[0]+1}. {mr[1].attrib['name']}/{mr[1].attrib['type']}: {mr[1].attrib['x']};{mr[1].attrib['y']}")
					if not merchants:
						print("Торговцев на карте не обнаружено")
					else:
						print("\n".join(merchants))
				if t == 5:
					ev = []
					for objects in root.findall('objectgroup'):
						for i in enumerate(objects):
							if i[1].attrib['type'] != "TradeZone":
								ev.append(f"-- {i[1].attrib['name']}/{i[1].attrib['type']}: {i[1].attrib['x']};{i[1].attrib['y']}")
					if not ev:
						print("Ничего на карте не обнаружено")
					else:
						print("\n".join(ev))
				if t == 9:
					break
		elif a == 4:
			for objects in root.findall('objectgroup'):
				if objects.attrib['name'] == "Players":
					for pl in objects:
						objects.remove(pl)
			tree.write("session.tmx", "UTF-8")
			print("Объекты игроков удалены с карты")
		elif a == 5:
			while True:
				coords = input("\nКоординаты клетки начала (x;y): ")
				if not coords:
					break
				coords = coords.split(";")
				try:
					x = int(coords[0])
					y = int(coords[1])
				except ValueError:
					print("Неверно введены координаты")
					continue
				try:
					width = int(input("Ширина зоны: "))
					height = int(input("Высота зоны: "))
					if width <= 0 or height <= 0:
						print("Высота или ширина должна быть больше нуля")
						continue
				except ValueError:
					print("Неверно введён параметр")
					continue
				w = []
				h = []
				for i in range(width):
					w.append(dict(x=x+i, y=y))
				for i in range(1, height):
					h.append(dict(y=y+i))
				for objects in root.findall('objectgroup'):
					if objects.attrib['name'] == "TradeZones":
						for xx in w:
							ET.SubElement(objects, 'object', {"name": "", "type": "TradeZone", "x": f"{xx['x']}", "y": f"{xx['y']}", 'width': '1', 'height': '1'})
							for yy in h:
								ET.SubElement(objects, 'object', {"name": "", "type": "TradeZone", "x": f"{xx['x']}", "y": f"{yy['y']}", 'width': '1', 'height': '1'})
				w.clear()
				h.clear()
				tree.write("session.tmx", "UTF-8")
				print("Торговая зона успешно создана")
		elif a == 6:
			while True:
				coords = input("\nКоординаты клетки (x;y): ")
				if not coords:
					break
				coords = coords.split(";")
				try:
					x = int(coords[0])
					y = int(coords[1])
				except ValueError:
					print("Неверно введены координаты")
					continue
				p = True
				for objects in root.findall('objectgroup'):
					for i in objects:
						if int(i.attrib['x']) == x and int(i.attrib['y']) == y:
							print(f"Здесь уже находится объект: {i.attrib['name']} // {i.attrib['type']}")
							p = False
				if not p:
					continue
				try:
					sqType = int(input("Тип клетки:\n1. Сундук\n2. Пустой торговец\n3. Заполненый торговец\n4. Тесто\n9. Выход\n>>>"))
				except ValueError:
					print("Ошибка в вводе ответа")
					continue
				if sqType == 1:
					try:
						chType = int(input("Тип сундука:\n1. Standart\n2. Rare\n3. Exclusive\n4. Absolute\n5. Отмена\n>>>"))
					except ValueError:
						print("Ошибка в вводе ответа")
						continue
					for objects in root.findall('objectgroup'):
						if objects.attrib['name'] == "Chests":
							for i in objects:
								if chType == 1:
									ET.SubElement(objects, "object", {"name": "Chest", "type": "ClosedStandart",  'x': str(x), 'y': str(y), 'width': '1', 'height': '1'})
								elif chType == 2:
									ET.SubElement(objects, "object", {"name": "Chest", "type": "ClosedRare",  'x': str(x), 'y': str(y), 'width': '1', 'height': '1'})
								elif chType == 3:
									ET.SubElement(objects, "object", {"name": "Chest", "type": "ClosedExclusive",  'x': str(x), 'y': str(y), 'width': '1', 'height': '1'})
								elif chType == 4:
									ET.SubElement(objects, "object", {"name": "Chest", "type": "ClosedAbsolute",  'x': str(x), 'y': str(y), 'width': '1', 'height': '1'})
								tree.write("session.tmx", "UTF-8")
								if chType in [1, 2, 3, 4]: 
									print("Объект создан")
								break
		elif a == 7:
			while True:
				plid = input("\nID игрока: ")
				if not plid:
					break
				try:
					plid = int(plid)
				except ValueError:
					print("ID игрока введён некорректно")
					continue
				p = False
				for i in root.findall("objectgroup"):
					if i.attrib['name'] == "Players":
						for pl in i:
							if pl.attrib['name'] == str(plid):
								while True:
									coords = input("\nКоординаты клетки для телепорта (x;y): ")
									if not coords:
										break
									coords = coords.split(";")
									try:
										x = int(coords[0])
										y = int(coords[1])
									except ValueError:
										print("Неверно введены координаты")
										continue
									pl.set("x", f"{x}")
									pl.set("y", f"{y}")
									tree.write("session.tmx", "UTF-8")
									p = True
									break
				if p:
					print("Игрок перемещён")
				else:
					print("Игрок не найден на карте")
		elif a == 9:
			break

if __name__ == "__main__":
	main()
