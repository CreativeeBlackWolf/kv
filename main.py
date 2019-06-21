import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sys
import os
import sessionhandler as sh
from utils import *
import random
import versions as ver
import commands as com
from importlib import reload

ingame = []

comhelp = {
	'help': 'show the help message for command/to see commands list // ~help [command]',
	'pingS': 'u can\'t write "~ping"?',
	'ping': 'just ping the bot // ~ping',
	'register': 'register the account // ~register',
	'deleteacc': 'delete the account // ~deleteacc',
	'ruleofinternet': 'check the interesting rule (ex. 34) // ~rofi or ~ruleofinternet + (number/"random")',
	'whereami': 'we know where are you (x;y) // ~whereami',
	'showinv': 'see your inv. // ~showinv',
	'tradeinv': 'see your trade inv. // ~tradeinv',
	'gamehelp': 'help for ingame commands // ~gamehelp [command]',
	'socialhelp': 'help for social commands // ~socialhelp [command]',
	'loli': 'catch the random loli // ~loli',
	'version': 'find out account version // ~version',
	'upgrade': 'upgrate to latest account version // ~upgrade'
}

gamehelp = {
	'enter': 'enter to the world! // !enter',
	'move': 'move is some direction // !move (right, left, up, down)',
	'leave': 'leave the session // !leave',
	'tileplayers': 'see all players on your tile // !tileplayers',
	'save': 'save your position // !save',
	'open': 'open the chest if u\'re on it // !open',
	'action': 'action w/ item in inventory // !action (item number in inv.)',
	'itemlist': 'check the item list in the shop // !itemlist',
	'buy': 'buy the item // !buy (item number in merchant\'s inv.)',
	'sell': 'sell the item // !sell (item number in inventory)'
}

sochelp = {
	'chat': 'chat with players on your tile (ONLY in game) // /chat (message)',
	'addfriend': 'send/accept friend request // /addfriend (ID)',
	'denyrequest': 'deny/cancel friend request // /denyrequest (ID)',
	'friendlist': 'your friend list // /friendlist',
	'me': 'do something in chat (like hug someone) (ONLY in game) // /me (action(message))',
	'pm': 'send private message to friend (ONLY in game) // /pm (friendID) (message)',
	'removefriend': 'remove user from your friend list // /removefriend (friendID)',
	'sendmoney': 'send money to user // /sendmoney (userID) (count)',
	'sendgift': 'send gift to your friend // /sendgift (friendID) (item number in inventory) (message)'
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
				if len(event.text.split()) == 1:
					photo = random.choice(os.listdir("E:\\lolies"))
					onUpload = upload.photo_messages(photos="E:\\lolies\\" + photo)[0]
					vk.messages.send(user_id=uid, message="here's your random loli", attachment=f"photo{onUpload['owner_id']}_{onUpload['id']}")
				else:
					vk.messages.send(user_id=uid, message=comhelp['loli'])

			"""
			2 commands w/ secret syntax
			"""

			if event.text.startswith('~ping'):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message='понг блядь')
				else:
					vk.messages.send(user_id=uid, message=comhelp['pingS'])

			if event.text.startswith('~shutdown'):
				if event.user_id == cid:
					vk.messages.send(user_id=uid, message='Shutting down...')
					raise SystemExit

			if event.text.startswith('~restart'):
				if event.user_id == cid:
					if ingame:
						for i in ingame:
							ingame.remove(i)
							com.mapLeave(i)
							vk.messages.send(user_id=i, message="Your account has been forcibly removed from the session.")
							vk.messages.send(user_id=uid, message=f"{vk.users.get(user_ids=i)[0]['first_name']} был удалён из сессии")
					vk.messages.send(user_id=uid, message='Restarting bot...')
					with open('.rsttemp', 'w') as f:
						f.write(str(event.user_id))
					os.execv(sys.executable, ['python'] + sys.argv)

			if event.text.startswith('~reload'):
				if event.user_id == cid:
					if len(event.text.split()) == 2:
						if event.text.split()[1] in ["sh", "com", "ver", "utils"]:
							if event.text.split()[1] == "sh":
								reload(sh)
							if event.text.split()[1] == "com":
								reload(com)
							if event.text.split()[1] == "ver":
								reload(ver)
							if event.text.split()[1] == "utils":
								reload(utils)
							vk.messages.send(user_id=uid, message=f"Module \"{event.text.split()[1]}\" reloaded")
					else:
						vk.messages.send(user_id=uid, message="~reload (module)")

			if event.text.startswith('~ruleofinternet') or event.text.startswith('~rofi'):
				if len(event.text.split()) == 2:
					if event.text.split()[1] == 'random':
						randrule = str(random.randint(1, 49))
						vk.messages.send(user_id=uid, message=com.rofi(randrule))
					else:
						vk.messages.send(user_id=uid, message=com.rofi(event.text.split()[1]))
				else:
					vk.messages.send(user_id=uid, message=comhelp['ruleofinternet'])

			if event.text.startswith('~register'):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message=com.register(uid, userName, userLastName))
				else:
					vk.messages.send(user_id=uid, message=comhelp["register"])

			if event.text.startswith('~showinv'):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message=com.showInventory(uid))
				else:
					vk.messages.send(user_id=uid, message=comhelp["showinv"])

			if event.text.startswith('~deleteacc'):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message=com.delete(uid))
				else:
					vk.messages.send(user_id=uid, message=comhelp['deleteacc'])

			if event.text.startswith('~secretkitty'):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message="""
⊂_ヽ 
　 ＼＼  Λ＿Λ 
　　 ＼(　ˇωˇ)　 
　　　 　⌒ヽ 
　　　/ 　 へ＼ 
　　 /　　/　＼＼ 
　　 ﾚ　ノ　　 ヽ_つ 
　　/　/ 
　 /　/| 
　(　(ヽ 
　|　|、＼ 
　| 丿 ＼ ⌒) 
　| |　　) / 
`ノ )　　Lﾉ 
(_／
""")

			if event.text.startswith('~version'):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message=f"Account version: v.{checkVersion(uid)}\nLatest version: v.{ver.latestVersion}")
				else:
					vk.messages.send(user_id=uid, message=comhelp['version'])

			if event.text.startswith('~upgrade'):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message=ver.upgradeToLatest(uid))
				else:
					vk.messages.send(user_id=uid, message=comhelp['upgrade'])

			if event.text.startswith('!enter'):
				if len(event.text.split()) == 1:
					if uid not in ingame:
						ingame.append(uid)
						com.playerToMap(uid)
						vk.messages.send(user_id=uid, message="Account is now in session")
					else:
						vk.messages.send(user_id=uid, message="U're already in session")
				else:
					vk.messages.send(userid=uid, message=comhelp['enter'])

			if event.text.startswith("!move"):
				if uid in ingame:
					if len(event.text.split()) == 2:
						direction = event.text.split()[1].lower()
						if direction in ['right', 'left', 'up', 'down']:
							vk.messages.send(user_id=uid, message=sh.move(uid, direction))
						else:
							vk.messages.send(user_id=uid, message="Wrong direction, enter one of the 'right', 'left', 'up', 'down'")
				else:
					vk.messages.send(user_id=uid, message="You must be in session")

			if event.text.startswith("!open"):
				if checkVersion(uid) >= 51:
					if uid in ingame:
						if len(event.text.split()) == 1:
							vk.messages.send(user_id=uid, message=sh.openChest(uid))
						else:
							vk.messages.send(user_id=uid, message=gamehelp['open'])
					else:
						vk.messages.send(user_id=uid, message="You must be in session")
				else:
					vk.messages.send(user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

			if event.text.startswith("!action"):
				if uid in ingame:
					if len(event.text.split()) == 2:
						vk.messages.send(user_id=uid, message=sh.itemAction(uid, event.text.split()[1]))
					else:
						vk.messages.send(user_id=uid, message=gamehelp['action'])
				else:
					vk.messages.send(user_id=uid, message="You must be in session")

			if event.text.startswith("!itemlist"):
				if uid in ingame:
					if len(event.text.split()) == 1:
						vk.messages.send(user_id=uid, message=com.showShopList(uid))
					else:
						vk.messages.send(user_id=uid, message=gamehelp['itemlist'])
				else:
					vk.messages.send(user_id=uid, message="You must be in session")

			if event.text.startswith("!buy"):
				if checkVersion(uid) >= 51:
					if uid in ingame:
						if len(event.text.split()) == 2:
							vk.messages.send(user_id=uid, message=com.buyItem(uid, event.text.split()[1]))
						else:
							vk.messages.send(user_id=uid, message=gamehelp['buy'])
					else:
						vk.messages.send(user_id=uid, message="You must be in session")
				else:
					vk.messages.send(user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

			if event.text.startswith("!sell"):
				if checkVersion(uid) >= 51:
					if uid in ingame:
						if len(event.text.split()) == 2:
							vk.messages.send(user_id=uid, message=com.sellItem(uid, event.text.split()[1]))
						else:
							vk.messages.send(user_id=uid, message=gamehelp['sell'])
					else:
						vk.messages.send(user_id=uid, message="You must be in session")
				else:
					vk.messages.send(user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

			if event.text.startswith("~tradeinv"):
				if checkVersion(uid) >= 51:
					if len(event.text.split()) == 1:
						vk.messages.send(user_id=uid, message=com.showTradeInventory(uid))
					else:
						vk.messages.send(user_id=uid, message=comhelp['tradeinv'])
				else:
					vk.messages.send(user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

			if event.text.startswith("!tileplayers"):
				if uid in ingame:
					if len(event.text.split()) == 1:
						vk.messages.send(user_id=uid, message=com.playersOnTile(uid))
					else:
						vk.messages.send(user_id=uid, message=gamehelp['tileplayers'])
				else:
					vk.messages.send(user_id=uid, message="You must be in session")

			if event.text.startswith("/pm"):
				if uid in ingame:
					if len(event.text.split()) > 2:
						if int(event.text.split()[1]) not in ingame:
							vk.messages.send(user_id=uid, message="User isn't in game")
						else:
							if inFriends(uid, event.text.split()[1]):
								vk.messages.send(user_id=event.text.split()[1], message=f"{com.searchByID(uid)}(PM): {' '.join(event.text.split()[2:])}")
								vk.messages.send(user_id=uid, message=f"{com.searchByID(uid)}(PM): {event.text.split()[2:]}")
							else:
								vk.messages.send(user_id=uid, message="This user isn't in your friendlist")
					else:
						vk.messages.send(user_id=uid, message=sochelp['pm'])
				else:
					vk.messages.send(user_id=uid, message="You must be in session")

			if event.text.startswith("/sendmoney"):
				if len(event.text.split()) == 3:
					vk.messages.send(user_id=uid, message=com.sendMoney(uid, event.text.split()[1], event.text.split()[2]))
				else:
					vk.messages.send(user_id=uid, message=sochelp['sendmoney'])

			if event.text.startswith("/sendgift"):
				if isExist(uid):
					if checkVersion(uid) >= 51:
						if len(event.text.split()) >= 3:
							if checkVersion(event.text.split()[1]) >= 51:
								vk.messages.send(user_id=uid, message=com.sendGift(uid, event.text.split()[1], event.text.split()[2], event.text.split()[3:]))
							else:
								vk.messages.send(user_id=uid, message="This account have version lower than 51 or not registered")
						else:
							vk.messages.send(user_id=uid, message=sochelp['sendgift'])
					else:
						vk.messages.send(user_id=uid, message="Upgrade account to the latest version with '~upgrade' command.")
				else:
					vk.messages.send(user_id=uid, message="Register first")

			if event.text.startswith("/acceptgift"):
				if isExist(uid):
					if checkVersion(uid) >= 51:
						if len(event.text.split()) == 2:
							vk.messages.send(user_id=uid, message=com.acceptGift(uid, event.text.split()[1]))
						else:
							vk.messages.send(user_id=uid, message=sochelp['acceptgift'])
					else:
						vk.messages.send(user_id=uid, message="Upgrade account to the latest version with '~upgrade' command.")
				else:
					vk.messages.send(user_id=uid, message="Register first")

			if event.text.startswith("/rejectgift"):
				if isExist(uid):
					if checkVersion(uid) >= 51:
						if len(event.text.split()) == 2:
							vk.messages.send(user_id=uid, message=com.rejectGift(uid, event.text.split()[1]))
						else:
							vk.messages.send(user_id=uid, message=sochelp['rejectgift'])
					else:
						vk.messages.send(user_id=uid, message="Upgrade account to the latest version with '~upgrade' command.")
				else:
					vk.messages.send(user_id=uid, message="Register first")

			if event.text.startswith("/chat"):
				if uid in ingame:
					if len(event.text.split()) == 1:
						vk.messages.send(user_id=uid, message="You don't wrote the message")
					else:
						sh.chat(uid, event.text.split()[1:], False)
				else:
					vk.messages.send(user_id=uid, message="You must be in session")

			if event.text.startswith("/me"):
				if uid in ingame:
					if len(event.text.split()) == 1:
						vk.messages.send(user_id=uid, message="You don't wrote the message")
					else:
						sh.chat(uid, event.text.split()[1:], True)
				else:
					vk.messages.send(user_id=uid, message="You must be in session")

			if event.text.startswith("/addfriend"):
				if len(event.text.split()) == 2:
					vk.messages.send(user_id=uid, message=com.addFriend(uid, event.text.split()[1]))
				else:
					vk.messages.send(user_id=uid, message=sochelp['addfriend'])

			if event.text.startswith("/denyrequest"):
				if len(event.text.split()) == 2:
					vk.messages.send(user_id=uid, message=com.denyFriendRequest(uid, event.text.split()[1]))
				else:
					vk.messages.send(user_id=uid, message=sochelp['denyrequest'])

			if event.text.startswith("/friendlist"):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message=com.friendList(uid))
				else:
					vk.messages.send(user_id=uid, message=sochelp['friendlist'])

			if event.text.startswith("/removefriend"):
				if len(event.text.split()) == 2:
					vk.messages.send(user_id=uid, message=com.removeFriend(uid, event.text.split()[1]))
				else:
					vk.messages.send(user_id=uid, message=sochelp['removefriend'])

			if event.text.startswith('!leave'):
				if len(event.text.split()) == 1:
					if uid in ingame:
						ingame.remove(uid)
						com.mapLeave(uid)
						vk.messages.send(user_id=uid, message="Account removed from session")
					else:
						vk.messages.send(user_id=uid, message="Account isn't in session")
				else:
					vk.messages.send(user_id=uid, message=comhelp['leave'])

			if event.text.startswith("!save"):
				if len(event.text.split()) == 1:
					vk.messages.send(user_id=uid, message=com.save(uid))
				else:
					vk.messages.send(user_id=uid, message=gamehelp['save'])

			if event.text.startswith('~whereami'):
				if len(event.text.split()) == 1:
					kurwa = com.getCoords(uid)
					vk.messages.send(user_id=uid, message=f"You're on ({kurwa[0]};{kurwa[1]}) (x;y)")
				else:
					vk.messages.send(user_id=uid, message=comhelp['whereami'])

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
				if len(event.text.split()) == 1:
					msg = f"""These commands have the prefix "~"
help: {comhelp['help']}

gamehelp: {comhelp['gamehelp']}

socialhelp: {comhelp['socialhelp']}

ping: {comhelp['ping']}

register: {comhelp['register']}

deleteacc: {comhelp['deleteacc']}

version: {comhelp['version']}

upgrade: {comhelp['upgrade']}

showinv: {comhelp['showinv']}

tradeinv: {comhelp['tradeinv']}

ruleofinternet: {comhelp['ruleofinternet']}

loli: {comhelp['loli']}

whereami: {comhelp['whereami']}
"""
					vk.messages.send(user_id=uid, message=msg)
				elif len(event.text.split()) == 2:
					if event.text.split()[1] in comhelp:
						vk.messages.send(user_id=uid, message=comhelp[event.text.split()[1]])
					else:
						vk.messages.send(user_id=uid, message="Command is not found. Try ~help")

			if event.text.startswith("~gamehelp"):
				if len(event.text.split()) == 1:
					msg = f"""These commands have the prefix "!"
enter: {gamehelp['enter']}

move: {gamehelp['move']}

tileplayers: {gamehelp['tileplayers']}

leave: {gamehelp['leave']}

save: {gamehelp['save']}

open: {gamehelp['open']}

action: {gamehelp['action']}

itemlist: {gamehelp['itemlist']}

buy: {gamehelp['buy']}

sell: {gamehelp['sell']}
"""
					vk.messages.send(user_id=uid, message=msg)
				if len(event.text.split()) == 2:
					if event.text.split()[1] in gamehelp:
						vk.messages.send(user_id=uid, message=gamehelp[event.text.split()[1]])
					else:
						vk.messages.send(user_id=uid, message="Command is not found. Try ~gamehelp")

			if event.text.startswith("~socialhelp"):
				if len(event.text.split()) == 1:
					msg = f"""These commands have the prefix "/"
chat: {sochelp['chat']}

me: {sochelp['me']}

addfriend: {sochelp['addfriend']}

removefriend: {sochelp['removefriend']}

denyrequest: {sochelp['denyrequest']}

firendlist: {sochelp['friendlist']}

sendmoney: {sochelp['sendmoney']}

sendgift: {sochelp['sendgift']}
"""
					vk.messages.send(user_id=uid, message=msg)
				if len(event.text.split()) == 2:
					if event.text.split()[1] in sochelp:
						vk.messages.send(user_id=uid, message=sochelp[event.text.split()[1]])
					else:
						vk.messages.send(user_id=uid, message="Command is not found. Try ~socialhelp")

if __name__ == '__main__':
	main()
