import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sys
import os
import sessionhandler as sh
from shlex import split
import random
import commands as com

ingame = []

comhelp = {
	'help': 'show the help message for command/to see commands list // ~help [command]',
	'pingS': 'u can\'t write "~ping"?',
	'ping': 'just ping the bot // ~ping',
	'accRegister': 'enter the game // ~accRegister',
	'accDelete': 'delete the account // ~accDelete',
	'ruleofinternet': 'check the interesting rule (ex. 34) // ~rofi or ~ruleofinternet + (number/"random")',
	'getCoords': 'get your coords // ~getCoords',
	'gamehelp': 'help for ingame commands // ~gamehelp [command]',
	'loli': 'catch the random loli // ~loli'
}

gamehelp = {
	'enter': 'enter to the world! // !enter',
	'move': 'move is some direction // !move (right, left, up, down)',
	'leave': 'leave the session // !leave',
	'tileplayers': 'see all players on your tile // !tileplayers',
	'chat': 'chat with players on your tile // /chat (message)',
	'save': 'save your position // !save'
}

with open('token.txt', 'r') as f:
	token = f.read()
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def main():
	upload = vk_api.VkUpload(vk_session)
	with open('creator.txt', 'r') as c:
		cid = int(c.read())
	if os.path.isfile('.rsttemp'):
		with open('.rsttemp') as f:
			uid = f.read()
		os.remove('.rsttemp')
		vk.messages.send(user_id=uid, message="Bot restarted")
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text: #Слушаем longpoll, если пришло сообщение то:
			uid = event.user_id

			userData = vk.users.get(user_ids=uid)[0]
			userName = userData['first_name']
			userLastName = userData['last_name']

			if event.text.startswith("~loli"):
				if len(split(event.text)) == 1:
					photo = random.choice(os.listdir("E:\\lolies"))
					onUpload = upload.photo_messages(photos="E:\\lolies\\" + photo)[0]
					vk.messages.send(user_id=uid, message="here's your random loli", attachment=f"photo{onUpload['owner_id']}_{onUpload['id']}")
				else:
					vk.messages.send(user_id=uid, message=comhelp['loli'])

			"""
			2 commands w/ secret syntax
			"""

			if event.text.startswith('~ping'):
				if len(split(event.text)) == 1:
					vk.messages.send(user_id=uid, message='понг блядь')
				else:
					vk.messages.send(user_id=uid, message=comhelp['pingS'])

			if event.text.startswith('~shutdown'):
				if event.user_id == cid:
					vk.messages.send(user_id=uid, message='Shutting down...')
					raise SystemExit

			if event.text.startswith('~restart'):
				if event.user_id == cid:
					vk.messages.send(user_id=uid, message='Restarting bot...')
					with open('.rsttemp', 'w') as f:
						f.write(str(event.user_id))
					os.execv(sys.executable, ['python'] + sys.argv)

			if event.text.startswith('~ruleofinternet') or event.text.startswith('~rofi'):
				if len(split(event.text)) == 2:
					if split(event.text)[1] == 'random':
						randrule = str(random.randint(1, 49))
						vk.messages.send(user_id=uid, message=com.rofi(randrule))
					else:
						vk.messages.send(user_id=uid, message=com.rofi(split(event.text)[1]))
				else:
					vk.messages.send(user_id=uid, message=comhelp['ruleofinternet'])

			if event.text.startswith('~accRegister'):
				if len(split(event.text)) == 1:
					vk.messages.send(user_id=uid, message=com.register(uid, userName, userLastName))
				else:
					vk.messages.send(user_id=uid, message=comhelp["accRegister"])

			if event.text.startswith('~accDelete'):
				if len(split(event.text)) == 1:
					vk.messages.send(user_id=uid, message=com.delete(uid))
				else:
					vk.messages.send(user_id=uid, message=comhelp['accDelete'])

			if event.text.startswith('!enter'):
				if len(split(event.text)) == 1:
					if uid not in ingame:
						ingame.append(uid)
						com.playertomap(uid)
						vk.messages.send(user_id=uid, message="Account is now in session")
					else:
						vk.messages.send(user_id=uid, message="U're already in session")
				else:
					vk.messages.send(userid=uid, message=comhelp['enter'])

			if event.text.startswith("!move"):
				if uid in ingame:
					if len(split(event.text)) == 2:
						direction = split(event.text)[1].lower()
						if direction in ['right', 'left', 'up', 'down']:
							vk.messages.send(user_id=uid, message=sh.move(uid, direction))
						else:
							vk.messages.send(user_id=uid, message="Wrong direction, enter one of the 'right', 'left', 'up', 'down'")
				else:
					vk.messages.send(user_id=uid, message="Enter session first")

			if event.text.startswith("!tileplayers"):
				if uid in ingame:
					if len(split(event.text)) == 1:
						vk.messages.send(user_id=uid, message=com.playersOnTile(uid))
					else:
						vk.messages.send(user_id=uid, message=gamehelp['tileplayers'])
				else:
					vk.messages.send(user_id=uid, message="Enter session first")

			if event.text.startswith("/chat"):
				if uid in ingame:
					if len(event.text.split(" ")) == 1:
						vk.messages.send(user_id=uid, message="You don't wrote the message")
					else:
						sh.chat(uid, event.text.split(" ")[1:])
				else:
					vk.messages.send(user_id=uid, message="Enter session first")

			if event.text.startswith('!leave'):
				if len(split(event.text)) == 1:
					if uid in ingame:
						ingame.remove(uid)
						com.mapLeave(uid)
						vk.messages.send(user_id=uid, message="Account removed from session")
					else:
						vk.messages.send(user_id=uid, message="Account isn't in session")
				else:
					vk.messages.send(user_id=uid, message=comhelp['leave'])

			if event.text.startswith('~getCoords'):
				if len(split(event.text)) == 1:
					kurwa = com.getCoords(uid)
					vk.messages.send(user_id=uid, message=f"U're on ({kurwa[0]}; {kurwa[1]})")
				else:
					vk.messages.send(user_id=uid, message=comhelp['getCoords'])

			if event.text.startswith("~!!dropsession"):
				if event.user_id == cid:
					if ingame:
						for i in ingame:
							ingame.remove(i)
							com.mapLeave(i)
							vk.messages.send(user_id=i, message="Your account has been forcibly removed from the session.")
							vk.messages.send(user_id=uid, message=f"{vk.users.get(user_ids=i)[0]['first_name']} был удалён из сессии")
					else:
						vk.messages.send(user_id=uid, message='Никого в сессии нет, еблан')

			if event.text.startswith('~help'):
				if len(split(event.text)) == 1:
					msg = f"""These commands have the prefix "~":
help: {comhelp['help']}

gamehelp: {comhelp['gamehelp']}

ping: {comhelp['ping']}

accRegister: {comhelp['accRegister']}
|
accDelete: {comhelp['accDelete']}

ruleofinternet: {comhelp['ruleofinternet']}

loli: {comhelp['loli']}
"""
					vk.messages.send(user_id=uid, message=msg)
				elif len(split(event.text)) == 2:
					if split(event.text)[1] in comhelp:
						vk.messages.send(user_id=uid, message=comhelp[split(event.text)[1]])
					else:
						vk.messages.send(user_id=uid, message="Command is not found. Try ~help")

			if event.text.startswith("~gamehelp"):
				if len(split(event.text)) == 1:
					msg = f"""These commands have the prefix "!"
enter: {gamehelp['enter']}

move: {gamehelp['move']}

tileplayers: {gamehelp['tileplayers']}

leave: {gamehelp['leave']}

save: {gamehelp['save']}

Special commands (prefix "/"):
chat: {gamehelp['chat']}
"""
					vk.messages.send(user_id=uid, message=msg)
				if len(split(event.text)) == 2:
					if split(event.text)[1] in gamehelp:
						vk.messages.send(user_id = uid, message = gamehelp[split(event.text)[1]])
					else:
						vk.messages.send(user_id=uid, message="Command is not found. Try ~gamehelp")

if __name__ == '__main__':
	main()
