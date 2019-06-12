import xml.etree.cElementTree as ET


def main():
	while True:
		try:
			a = int(input("\nВыберите действие:\n1. Редактировать клетку\n2. Удалить клетку\n3. Просмотреть все объекты данного типа\n9. Выход\n>>>"))
		except:
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
				except:
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
									except:
										print("Неверно введён аргумент")
										break
									if typeEdit == 1:
										try:
											chestType = int(input("Тип сундука:\n1. ClosedStandart\n2. ClosedRare\n3. ClosedExclusive\n4. ClosedAbsolute\n5. Отмена\n>>>"))
										except:
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
										except:
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
				except:
					print("Неверно введены координаты")
					continue
				for objects in root.findall('objectgroup'):
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
					t = int(input("\nОбъекты:\n1. Игроки\n2. Триггеры\n3. Сундуки\n9. Выход\n>>>"))
				except:
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
				if t == 9:
					break
		elif a == 9:
			break

if __name__ == "__main__":
	main()
	#tree = ET.parse("session.tmx")
	#root = tree.getroot()
	#for objects in root.findall('objectgroup'):
	#	print(objects.attrib['name'])