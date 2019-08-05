from vk_api.longpoll import VkLongPoll, VkEventType
from time import gmtime, strftime
from importlib import reload
import vk_api
import sys
import os
import osu.calc as calc
import osucommands
import sessionhandler as sh
import utils as ut
import random
import urllib.request
import versions as ver
import commands as com

ingame = []

comhelp = {
	'help': 'show the help message for command/to see commands list // ~help | ~ [command or page number (2)]',
	'osuhelp': 'show the help message for osu-like commands // ~osuhelp | o! | o!help [command]',
	'pingS': 'u can\'t write "~ping"?',
	'ping': 'just ping the bot // ~ping',
	'ruleofinternet': 'check the interesting rule (ex. 34) // ~rofi | ~ruleofinternet (number/"random")',
	'gamehelp': 'help for ingame commands // ~gamehelp | ! | !help [command or page number(2, 3)]',
	'socialhelp': 'help for social commands // ~socialhelp | "/" | "/help" [command]',
	'loli': 'catch the random loli // ~loli',
	'upload': 'upload the picture to bot\'s drive // ~uploadone (photo attachment)',
	'uploadmany': 'upload the pictureS to bot\'s drive // ~uploadone (photo attachmentS)'
}

gamehelp = {
	'enter': 'enter to the world! // !enter',
	'version': 'find out account version // !version',
	'upgrade': 'upgrate to latest account version // !upgrade',
	'register': 'register the account // !register',
	'unregister': 'delete the account // !unregister',
	'whereami': 'we know where are you (x;y) // !whereami',
	'description': 'see item desc in ur inv. // !description',
	'tradeinv': 'see your trade inv. // !tradeinv',
	'showinv': 'see your inv. // !showinv',
	'move': 'move is some direction // !move (right, left, up, down)',
	'leave': 'leave the session // !leave',
	'tileplayers': 'see all players on your tile // !tileplayers',
	'save': 'save your position // !save',
	'open': 'open the chest if u\'re on it // !open',
	'action': 'action w/ item in inventory // !action (item number in inv.)',
	'itemlist': 'check the item list in the shop // !itemlist',
	'buy': 'buy the item // !buy (item number in merchant\'s inv.)',
	'sell': 'sell the item // !sell (item number in inventory)',
	'actlist': 'show the actions list that u can do // !actlist'
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

osuhelp = {
	'pp': 'check pp for map // o!pp (link) [args (check ~osuhelp pp)]',
	'ppextended': '''check pp for map // o!pp (link) [args (--oppai recommended)]
Arguments:
-m, --mods (HRHDDT-like)
-a, --acc (float number like, ex. 99.9 (if more then 100.0, equals to 100.0))
-o, --offline | --oppai (use the local calculation (also can calculate unranked maps))''',
	'register': 'register as user to get recent scores for your profile // o!register (Username or ID in osu!)',
	'recent': 'view your/user\'s recent score // o!recent [Username or ID in osu!]',
	'change': 'change your osu! profile // o!change (Username or ID in osu!)',
	'me': 'see your osu!profile // o!me',
	'changeavatar': 'redownload your avatar if you changed it // o!changeavatar'
}

with open('token.txt', 'r') as f:
	token = f.read()
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
print("Longpool authorized.")
vk = vk_session.get_api()
print("API things authorized.")

with open("usertoken.txt", "r") as uf:
	usertoken = uf.read()
uservkSession = vk_api.VkApi(token=usertoken)
uvk = uservkSession.get_api()
print("User API things authorized.")

def main():
	upload = vk_api.VkUpload(vk_session)
	with open('creator.txt', 'r') as c:
		cid = int(c.read())
	if os.path.isfile('.rsttemp'):
		with open('.rsttemp') as f:
			uid = f.read()
		os.remove('.rsttemp')
		vk.messages.send(random_id=0, user_id=uid, message="Bot restarted")
	print("---------------Rdy to use---------------")
	while True:
		try:
			for event in longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					uid = event.user_id
					osc = osucommands.commands(uid)
					userData = vk.users.get(user_ids=uid)[0]
					userName = userData['first_name']
					userLastName = userData['last_name']

					if event.text.startswith("~loli"):
						if len(event.text.split()) == 1:
							directory = "\\photos"
							photo = random.choice(os.listdir(directory))
							onUpload = upload.photo_messages(photos=directory + photo)[0]
							vk.messages.send(random_id=0, user_id=uid, message="here's your random loli", attachment=f"photo{onUpload['owner_id']}_{onUpload['id']}")
						else:
							vk.messages.send(random_id=0, user_id=uid, message=comhelp['loli'])

					if event.text.startswith("~uploadone"):
						if len(event.text.split()) == 1:
							if len(event.attachments) == 2:
								print(event.attachments)
								if event.attachments["attach1_type"] == "photo":
									photo = uvk.photos.getById(photos=event.attachments["attach1"])[0]["sizes"][-1]
									urllib.request.urlretrieve(photo["url"], os.path.join("photos", f"{photo['url'].split('/')[-1]}"))
									vk.messages.send(random_id=0, user_id=uid, message="Successfully uploaded on bot\'s drive")
								else:
									vk.messages.send(random_id=0, user_id=uid, message=f"The attachment type must be 'photo', not {event.attachments['attach1_type']}")
							else:
								vk.messages.send(random_id=0, user_id=uid, message="You can upload only one image")
						else:
							vk.messages.send(random_id=0, user_id=uid, message=comhelp["upload"])
					
					if event.text.startswith("~uploadmany"):
						if len(event.attachments) >= 2:
							urls = []
							for att in range(1, len(event.attachments) // 2 + 1):
								if event.attachments[f"attach{att}_type"] == "photo":
									urls.append(uvk.photos.getById(photos=event.attachments[f"attach{att}"])[0]["sizes"][-1]["url"])
								else:
									vk.messages.send(random_id=0, user_id=uid, message=f"Attachment {att} will not be uploaded (attachmentType:{event.attachments[f'attach{att}_type']})")
							if urls:
								dots = f"00.00%: 0/{len(urls)}"
								message = vk.messages.send(random_id=0, user_id=uid, message=f"{dots}")
								print(message)
								for url in enumerate(urls):
									urllib.request.urlretrieve(url[1], os.path.join("photos", f"{url[1].split('/')[-1]}"))
									dots = ("=" * url[0]) + ">"
									vk.messages.edit(peer_id=uid, message_id=message, message=f"{ut.toFixed((url[0]+1)/len(urls) * 100, 2)}% | {url[0]+1}/{len(urls)}")
								vk.messages.edit(peer_id=uid, message_id=message, message="Attachments uploaded to bot's drive")
								
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You don't attached anything")


					"""
					2 commands w/ secret syntax
					"""

					if event.text.startswith("o!pp"):
						if len(event.text.split()) >= 2:
							if ut.checkURL(event.text.split()[1]):
								stats = {"acc": 0.0, "mods": "", "combo": 0}
								if any(i in event.text.split() for i in ["-a", "—acc"]):
									a = "-a" if "-a" in event.text.split() else "—acc"
									ind = event.text.split().index(a)
									try:
										acc = float(event.text.split()[ind+1])
										stats["acc"] = acc
										if acc > 100:
											vk.messages.send(random_id=0, user_id=uid, message=f'Accuracy can\'t be more than 100% (entered {acc}), equate to 100%')
											stats["acc"] = 0.0
										if acc < 0:
											vk.messages.send(random_id=0, user_id=uid, message=f'Accuracy can\'t be less than 0% (entered {acc}), equate to {acc} module')										
											stats["acc"] = -acc
									except:
										vk.messages.send(random_id=0, user_id=uid, message='"acc" argument entered wrong')
								if "-combo" in event.text.split():
									ind = event.text.split().index("-combo")
									try:
										stats["combo"] = int(event.text.split()[ind+1])
									except:
										vk.messages.send(random_id=0, user_id=uid, message='"-combo" argument entered wrong')
								if any(i in event.text.split() for i in ["-m", "—mods"]):
									m = "-m" if "-m" in event.text.split() else "—mods"
									ind = event.text.split().index(m)
									if len(event.text.split()[ind+1]) <= 1:
										vk.messasges.send(random_id=0, user_id=uid, message='"mods" argument entered wrong')
									elif event.text.split()[ind+1].startswith('-'):
										vk.messasges.send(random_id=0, user_id=uid, message='"mods" argument entered wrong')									
									else:
										s = [event.text.split()[ind+1][i:i+2] for i in range(0, len(event.text.split()[ind+1]), 2)]
										wm = []
										if "HR" and "EZ" in s:
											vk.messages.send(random_id=0, user_id=uid, message="HR and EZ can't be in one selection")
											del s[random.choice(s.index("HR"), s.index("EZ"))]
										if "DT" and "HF" in s:
											vk.messages.send(random_id=0, user_id=uid, message="DT and HF can't be in one selection")
											del s[random.choice(s.index("DT"), s.index("HF"))]
										if "NF" and ("SD" or "PF") in s:
											vk.messages.send(random_id=0, user_id=uid, message="NF and SD/PF can't be in one selection")
										if "RX" in s or "AP" in s:
											vk.messages.send(random_id=0, user_id=uid, message="RX and AP mods aren't provided when calcucating pp")
										for i in s:
											if i.upper() == "RX":
												del s[s.index(i)]
											elif i.upper() == "AP":
												del s[s.index(i)]
											elif i.upper() == "SD":
												del s[s.index(i)]
												stats["misses"] = 0
											elif i.upper() == "PF":
												del s[s.index(i)]
												stats["acc"] = 0.0
											elif i.upper() in ["HR", "HD", "DT", "NC", "FL", "EZ", "NF", "HT"]:
												stats["mods"] += i.upper()
											else:
												wm.append(i)
										if wm:
											vk.messages.send(f"These mods aren't exist: {', '.join(wm)}")
								msg = event.text
								link = msg.split()[1]
								if not link.startswith("https://"):
									link = f"https://{link}"
								map = None
								if any(i in event.text.split() for i in ["-o", "—oppai", "—offline"]):	
									map = osc.calcOppai(link, acc=stats['acc'], mods=stats['mods'])
								if not map:
									if osc.checkStatus(link):
										map = osc.calcTillerino(link, acc=stats['acc'], mods=stats['mods'])
										if not map:
											message = vk.messages.send(random_id=0, user_id=uid, message="An error has occured when trying to do things w/ Tillerino API")
											map = calc.calcMap(link,
												acc=stats['acc'],
												combo=stats['combo'],
												amods=stats['mods'],
												uid=uid,
												messageid=message,
												t=token)
									else:
										map = "Beatmap status should be Ranked (or use -oppai)"
								if type(map) == dict:
									onUpload = None
									if not map:
										onUpload = upload.photo_messages(f"osu\\tmp\\dotosu\\Beatmap-{map['beatmapid']}\\thumbnail.jpg")[0]
									else:
										onUpload = upload.photo_messages(f"tmpthumbs\\{map['beatmapsetid']}.jpg")[0]
									length = strftime("%M:%S", gmtime(int(osucommands.getLength(map["beatmapid"]))))
									msg = f"""Title: {map['title']}
Length: {length}
AR: {map['AR']} | CS: {map['CS']} | OD: {map['OD']}
Stars: {map['stars']}	
Combo: {map['combo']}/{map['maxcombo']}
PP: """
									if len(map["PP"]) == 1:
										msg += f"{map['PP'][0]}\nAccuracy: {map['acc']}%"
									else:
										for i in enumerate(map['PP']):
											msg += f"{i[0]+95}%: {i[1]}pp | " if i[0] != len(map["PP"])-1 else f"{i[0]+95}%: {i[1]}pp"
									vk.messages.send(random_id=0, user_id=uid, message=msg,
													attachment=f"photo{onUpload['owner_id']}_{onUpload['id']}")
								else:
									vk.messages.send(random_id=0, user_id=uid, message=map)
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Please, recheck URL")
						else:
							vk.messages.send(random_id=0, user_id=uid, message=osuhelp["pp"])

					if event.text.split()[0] in ["o!r", "o!recent"]:
						if len(event.text.split()) == 1:
							d = osc.recentScore()
							if d[1]:
								onUpload = upload.photo_messages(f"tmpthumbs\\{d[1]}.jpg")[0]
								vk.messages.send(random_id=0, user_id=uid, message=d[0],
												attachment=f"photo{onUpload['owner_id']}_{onUpload['id']}")
							else:
								vk.messages.send(random_id=0, user_id=uid, message=d[0])
						if len(event.text.split()) == 2:
							d = osc.recentScore(event.text.split()[1])
							if d[1]:
								onUpload = upload.photo_messages(f"tmpthumbs\\{d[1]}.jpg")[0]
								vk.messages.send(random_id=0, user_id=uid, message=d[0],
												attachment=f"photo{onUpload['owner_id']}_{onUpload['id']}")
							else:
								vk.messages.send(random_id=0, user_id=uid, message=d[0])
						if len(event.text.split()) == 3:
							vk.messages.send(random_id=0, user_id=uid, message=osuhelp["recent"])

					if event.text.split()[0] in ["o!change", "o!c"]:
						if len(event.text.split()) == 2:
							vk.messages.send(random_id=0, user_id=uid, message=osucommands.change(uid, event.text.split()[1]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=osuhelp["change"])

					if event.text.split()[0] in ["o!reg", "o!register"]:
						if len(event.text.split()) == 2:
							vk.messages.send(random_id=0, user_id=uid, message=osucommands.register(uid, event.text.split()[1]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=osuhelp["register"])

					if event.text.startswith("o!changeavatar"):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=osc.changeAvatar())
						else:
							vk.messages.send(random_id=0, user_id=uid, message=osuhelp["changeavatar"])

					if event.text.startswith("o!me"):
						if len(event.text.split()) == 1:
							user = osc.me()
							if type(user) == dict:
								onUpload = upload.photo_messages(user["avatarPath"])[0]
								if user["username"].lower().endswith("s"):
									user["username"] += "'"
								else:
									user["username"] += "'s"
								msg = f"""{user["username"]} profile

PP: {user["pp"]}
Accuracy: {user["acc"]}%
Level: {user["level"]}
Global Rank / Country Rank: #{user["rank"]} / #{user["countryrank"]} ({user["country"]})
{user["playcount"]} plays total
Hits: {user["x300"]} x300 | {user["x100"]} x100 | {user["x50"]} x50

SS/SSH ranks: {user["SS"]} / {user["SSH"]}
S/SH ranks: {user["S"]} / {user["SH"]}
A ranks: {user["A"]}
"""
								vk.messages.send(random_id=0, user_id=uid, message=msg,
												attachment=f"photo{onUpload['owner_id']}_{onUpload['id']}")
						else:
							vk.messages.send(random_id=0, user_id=uid, message=osuhelp["me"])

					if event.text.startswith("!test"):
						if len(event.text.split()) >= 2:
							print(event.text.split())
						else:
							vk.messages.send(random_id=0, user_id=uid, message='n')

					if event.text.startswith('~ping'):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message='понг блядь')
						else:
							vk.messages.send(random_id=0, user_id=uid, message=comhelp['pingS'])

					if event.text.startswith('~shutdown'):
						if event.user_id == cid:
							vk.messages.send(random_id=0, user_id=uid, message='Shutting down...')
							raise SystemExit

					if event.text.startswith('~restart'):
						if event.user_id == cid:
							if ingame:
								for i in ingame:
									ingame.remove(i)
									com.mapLeave(i)
									vk.messages.send(random_id=0, user_id=i, message="Your account has been forcibly removed from the session.")
									vk.messages.send(random_id=0, user_id=uid, message=f"{vk.users.get(user_ids=i)[0]['first_name']} был удалён из сессии")
							vk.messages.send(random_id=0, user_id=uid, message='Restarting bot...')
							print("Started restart")
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
									vk.messages.send(random_id=0, user_id=uid, message=f"Module \"{event.text.split()[1]}\" reloaded")
							else:
								vk.messages.send(random_id=0, user_id=uid, message="~reload (module)")

					if event.text.startswith('~ruleofinternet') or event.text.startswith('~rofi'):
						if len(event.text.split()) == 2:
							if event.text.split()[1] == 'random':
								randrule = str(random.randint(1, 49))
								vk.messages.send(random_id=0, user_id=uid, message=com.rofi(randrule))
							else:
								vk.messages.send(random_id=0, user_id=uid, message=com.rofi(event.text.split()[1]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=comhelp['ruleofinternet'])

					if event.text.startswith('!register'):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=com.register(uid, userName, userLastName))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp["register"])

					if event.text.startswith('!showinv'):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=com.showInventory(uid))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp["showinv"])

					if event.text.startswith('!unregister'):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=com.delete(uid))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp['unregister'])

					if event.text.startswith('~secretkitty'):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message="""
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

					if event.text.startswith('!version'):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=f"Account version: v.{ut.checkVersion(uid)}\nLatest version: v.{ver.latestVersion}")
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp['version'])

					if event.text.startswith('!upgrade'):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=ver.upgradeToLatest(uid))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp['upgrade'])

					if event.text.startswith('!enter'):
						if len(event.text.split()) == 1:
							if uid not in ingame:
								ingame.append(uid)
								com.playerToMap(uid)
								vk.messages.send(random_id=0, user_id=uid, message="Account is now in session")
							else:
								vk.messages.send(random_id=0, user_id=uid, message="U're already in session")
						else:
							vk.messages.send(random_id=0, userid=uid, message=comhelp['enter'])

					if event.text.startswith("!actlist"):
						if uid in ingame:
							if len(event.text.split()) == 1:
								vk.messages.send(random_id=0, user_id=uid, message=com.actions(uid))
							else:
								vk.messages.send(random_id=0, user_id=uid, message=gamehelp["actlist"])
						else:
							vk.messages.send(random_id=27, user_id=uid, message="You must be in session")

					if event.text.startswith("!move"):
						if uid in ingame:
							if len(event.text.split()) == 2:
								direction = event.text.split()[1].lower()
								if direction in ['right', 'left', 'up', 'down']:
									vk.messages.send(random_id=0, user_id=uid, message=sh.move(uid, direction))
								else:
									vk.messages.send(random_id=0, user_id=uid, message="Wrong direction, enter one of the 'right', 'left', 'up', 'down'")
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You must be in session")

					if event.text.startswith("!open"):
						if ut.checkVersion(uid) >= ver.latestVersion:
							if uid in ingame:
								if len(event.text.split()) == 1:
									vk.messages.send(random_id=0, user_id=uid, message=sh.openChest(uid))
								else:
									vk.messages.send(random_id=0, user_id=uid, message=gamehelp['open'])
							else:
								vk.messages.send(random_id=0, user_id=uid, message="You must be in session")
						else:
							vk.messages.send(random_id=0, user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

					if event.text.startswith("!description"):
						if len(event.text.split()) == 2:
							vk.messages.send(random_id=0, user_id=uid, message=com.itemDesc(uid, event.text.split()[1]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp['description'])

					if event.text.startswith("!action"):
						if uid in ingame:
							if len(event.text.split()) == 2:
								vk.messages.send(random_id=0, user_id=uid, message=sh.itemAction(uid, event.text.split()[1]))
							else:
								vk.messages.send(random_id=0, user_id=uid, message=gamehelp['action'])
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You must be in session")

					if event.text.startswith("!itemlist"):
						if uid in ingame:
							if len(event.text.split()) == 1:
								vk.messages.send(random_id=0, user_id=uid, message=com.showShopList(uid))
							else:
								vk.messages.send(random_id=0, user_id=uid, message=gamehelp['itemlist'])
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You must be in session")

					if event.text.startswith("!buy"):
						if ut.checkVersion(uid) >= ver.latestVersion:
							if uid in ingame:
								if len(event.text.split()) == 2:
									vk.messages.send(random_id=0, user_id=uid, message=com.buyItem(uid, event.text.split()[1]))
								else:
									vk.messages.send(random_id=0, user_id=uid, message=gamehelp['buy'])
							else:
								vk.messages.send(random_id=0, user_id=uid, message="You must be in session")
						else:
							vk.messages.send(random_id=0, user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

					if event.text.startswith("!sell"):
						if ut.checkVersion(uid) >= ver.latestVersion:
							if uid in ingame:
								if len(event.text.split()) == 2:
									vk.messages.send(random_id=0, user_id=uid, message=com.sellItem(uid, event.text.split()[1]))
								else:
									vk.messages.send(random_id=0, user_id=uid, message=gamehelp['sell'])
							else:
								vk.messages.send(random_id=0, user_id=uid, message="You must be in session")
						else:
							vk.messages.send(random_id=0, user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

					if event.text.startswith("!tradeinv"):
						if ut.checkVersion(uid) >= ver.latestVersion:
							if len(event.text.split()) == 1:
								vk.messages.send(random_id=0, user_id=uid, message=com.showTradeInventory(uid))
							else:
								vk.messages.send(random_id=0, user_id=uid, message=gamehelp['tradeinv'])
						else:
							vk.messages.send(random_id=0, user_id=uid, message="Upgrade account to the latest version with '~upgrade' command")

					if event.text.startswith("!tileplayers"):
						if uid in ingame:
							if len(event.text.split()) == 1:
								vk.messages.send(random_id=0, user_id=uid, message=com.playersOnTile(uid))
							else:
								vk.messages.send(random_id=0, user_id=uid, message=gamehelp['tileplayers'])
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You must be in session")

					if event.text.startswith("/pm"):
						if uid in ingame:
							if len(event.text.split()) > 2:
								if int(event.text.split()[1]) not in ingame:
									vk.messages.send(random_id=0, user_id=uid, message="User isn't in game")
								else:
									if ut.inFriends(uid, event.text.split()[1]):
										vk.messages.send(random_id=0, user_id=event.text.split()[1], message=f"{com.searchByID(uid)}(PM): {' '.join(event.text.split()[2:])}")
										vk.messages.send(random_id=0, user_id=uid, message=f"{com.searchByID(uid)}(PM): {event.text.split()[2:]}")
									else:
										vk.messages.send(random_id=0, user_id=uid, message="This user isn't in your friendlist")
							else:
								vk.messages.send(random_id=0, user_id=uid, message=sochelp['pm'])
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You must be in session")

					if event.text.startswith("/sendmoney"):
						if len(event.text.split()) == 3:
							vk.messages.send(random_id=0, user_id=uid, message=com.sendMoney(uid, event.text.split()[1], event.text.split()[2]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=sochelp['sendmoney'])

					if event.text.startswith("/sendgift"):
						if ut.isExist(uid):
							if ut.checkVersion(uid) >= ver.latestVersion:
								if len(event.text.split()) >= 3:
									if ut.checkVersion(event.text.split()[1]) >= 51:
										vk.messages.send(random_id=0, user_id=uid, message=com.sendGift(uid, event.text.split()[1], event.text.split()[2], event.text.split()[3:]))
									else:
										vk.messages.send(random_id=0, user_id=uid, message="This account have version lower than 51 or not registered")
								else:
									vk.messages.send(random_id=0, user_id=uid, message=sochelp['sendgift'])
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Upgrade account to the latest version with '~upgrade' command.")
						else:
							vk.messages.send(random_id=0, user_id=uid, message="Register first")

					if event.text.startswith("/acceptgift"):
						if ut.isExist(uid):
							if ut.checkVersion(uid) >= ver.latestVersion:
								if len(event.text.split()) == 2:
									vk.messages.send(random_id=0, user_id=uid, message=com.acceptGift(uid, event.text.split()[1]))
								else:
									vk.messages.send(random_id=0, user_id=uid, message=sochelp['acceptgift'])
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Upgrade account to the latest version with '~upgrade' command.")
						else:
							vk.messages.send(random_id=0, user_id=uid, message="Register first")

					if event.text.startswith("/rejectgift"):
						if isExist(uid):
							if ut.checkVersion(uid) >= ver.latestVersion:
								if len(event.text.split()) == 2:
									vk.messages.send(random_id=0, user_id=uid, message=com.rejectGift(uid, event.text.split()[1]))
								else:
									vk.messages.send(random_id=0, user_id=uid, message=sochelp['rejectgift'])
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Upgrade account to the latest version with '~upgrade' command.")
						else:
							vk.messages.send(random_id=0, user_id=uid, message="Register first")

					if event.text.startswith("/chat"):
						if uid in ingame:
							if len(event.text.split()) == 1:
								vk.messages.send(random_id=0, user_id=uid, message="You don't wrote the message")
							else:
								sh.chat(uid, event.text.split()[1:], False)
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You must be in session")

					if event.text.startswith("/me"):
						if uid in ingame:
							if len(event.text.split()) == 1:
								vk.messages.send(random_id=0, user_id=uid, message="You don't wrote the message")
							else:
								sh.chat(uid, event.text.split()[1:], True)
						else:
							vk.messages.send(random_id=0, user_id=uid, message="You must be in session")

					if event.text.startswith("/addfriend"):
						if len(event.text.split()) == 2:
							vk.messages.send(random_id=0, user_id=uid, message=com.addFriend(uid, event.text.split()[1]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=sochelp['addfriend'])

					if event.text.startswith("/denyrequest"):
						if len(event.text.split()) == 2:
							vk.messages.send(random_id=0, user_id=uid, message=com.denyFriendRequest(uid, event.text.split()[1]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=sochelp['denyrequest'])

					if event.text.startswith("/friendlist"):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=com.friendList(uid))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=sochelp['friendlist'])

					if event.text.startswith("/removefriend"):
						if len(event.text.split()) == 2:
							vk.messages.send(random_id=0, user_id=uid, message=com.removeFriend(uid, event.text.split()[1]))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=sochelp['removefriend'])

					if event.text.startswith('!leave'):
						if len(event.text.split()) == 1:
							if uid in ingame:
								ingame.remove(uid)
								com.mapLeave(uid)
								vk.messages.send(random_id=0, user_id=uid, message="Account removed from session")
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Account isn't in session")
						else:
							vk.messages.send(random_id=0, user_id=uid, message=comhelp['leave'])

					if event.text.startswith("!save"):
						if len(event.text.split()) == 1:
							vk.messages.send(random_id=0, user_id=uid, message=com.save(uid))
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp['save'])

					if event.text.startswith('!whereami'):
						if len(event.text.split()) == 1:
							kurwa = com.getCoords(uid)
							vk.messages.send(random_id=0, user_id=uid, message=f"You're on ({kurwa[0]};{kurwa[1]}) (x;y)")
						else:
							vk.messages.send(random_id=0, user_id=uid, message=gamehelp['whereami'])

					if event.text.startswith("~!!dropsession"):
						if event.user_id == cid:
							if ingame:
								for i in ingame:
									ingame.remove(i)
									com.mapLeave(i)
									vk.messages.send(random_id=0, user_id=i, message="Your account has been forcibly removed from the session.")
									vk.messages.send(random_id=0, user_id=uid, message=f"{vk.users.get(user_ids=i)[0]['first_name']} был удалён из сессии")
							else:
								vk.messages.send(random_id=0, user_id=uid, message='Никого в сессии нет, еблан')

					if event.text.split()[0] in ["~", "~help"]:
						if len(event.text.split()) == 1:
							msg = f"""These commands have the prefix "~":
help: {comhelp['help']}

osuhelp: {comhelp['osuhelp']}

gamehelp: {comhelp['gamehelp']}

socialhelp: {comhelp['socialhelp']}

ping: {comhelp['ping']}

uploadmany: {comhelp['uploadmany']}
		"""
							vk.messages.send(random_id=0, user_id=uid, message=msg)
						elif len(event.text.split()) == 2:
							if event.text.split()[1] in comhelp:
								vk.messages.send(random_id=0, user_id=uid, message=comhelp[event.text.split()[1]])
							if int(event.text.split()[1]) in [2]:
								if int(event.text.split()[1]) == 2:
									msg = f"""~help page 2:

description: {comhelp['description']}

ruleofinternet: {comhelp['ruleofinternet']}

loli: {comhelp['loli']}

uploadone: {comhelp['upload']}
"""
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Command is not found. Try ~help")

					if event.text.split()[0] in ["!", "~gamehelp", "!help"]:
						if len(event.text.split()) == 1:
							msg = f"""These commands have the prefix "!"

register: {gamehelp['register']}

unregister: {gamehelp['unregister']}

version: {gamehelp['version']}

upgrade: {gamehelp['upgrade']}

enter: {gamehelp['enter']}

leave: {gamehelp['leave']}

whereami: {gamehelp['whereami']}

move: {gamehelp['move']}
"""
							vk.messages.send(random_id=0, user_id=uid, message=msg)
						if len(event.text.split()) == 2:
							if event.text.split()[1] in gamehelp:
								vk.messages.send(random_id=0, user_id=uid, message=gamehelp[event.text.split()[1]])
							if int(event.text.split()[1]) in [2, 3]:
								if int(event.text.split()[1]) == 2:
									msg = f"""~gamehelp page 2:
save: {gamehelp['save']}

open: {gamehelp['open']}

showinv: {gamehelp['showinv']}

tradeinv: {gamehelp['tradeinv']}

action: {gamehelp['action']}

itemlist: {gamehelp['itemlist']}

buy: {gamehelp['buy']}

sell: {gamehelp['sell']}
"""
									vk.messages.send(random_id=0, user_id=uid, message=msg)
								if int(event.text.split()[1]) == 3:
									msg = f"""~gamehelp page 3:
tileplayers: {gamehelp['tileplayers']}
"""
									vk.messages.send(random_id=0, user_id=uid, message=msg)
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Command is not found. Try ~gamehelp")

					if event.text.split()[0] in ["/", "~socialhelp", "/help"]:
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
							vk.messages.send(random_id=0, user_id=uid, message=msg)
						if len(event.text.split()) == 2:
							if event.text.split()[1] in sochelp:
								vk.messages.send(random_id=0, user_id=uid, message=sochelp[event.text.split()[1]])
							else:
								vk.messages.send(random_id=0, user_id=uid, message="Command is not found. Try ~socialhelp")

					if event.text.split()[0] in ["o!", "~osuhelp", "o!help"]:
						if len(event.text.split()) == 1:	
							msg = f"""These commands have the prefix "o!"
pp: {osuhelp["pp"]}

register: {osuhelp["register"]}

change: {osuhelp["change"]}

recent: {osuhelp["recent"]}

me: {osuhelp["me"]}

changeavatar: {osuhelp["changeavatar"]}
"""							
							vk.messages.send(random_id=0, user_id=uid, message=msg)
						if len(event.text.split()) == 2:
							if event.text.split()[1] == "pp":
								vk.messages.send(random_id=0, user_id=uid, message=osuhelp["ppextended"])
							else:
								if event.text.split()[1] in osuhelp and event.text.split()[1] != "pp":
									vk.messages.send(random_id=0, user_id=uid, message=osuhelp[event.text.split()[1]])
								else:
									vk.messages.send(random_id=0, user_id=uid, message="Commands is not found. Try ~osuhelp")

		except UnboundLocalError as e:
			print(f"Catched a UnboundLocalError exception, restart: {e}")
			continue
		except TypeError as e:
			print(f"Catched a TypeError exception, restart: {e}")
			continue
		except NameError as e:
			print(f"Catched a NameError exception, restart: {e}")
			continue
		except KeyError as e:
			print(f"Catched a KeyError exception, restart: {e}")
			continue
		except ZeroDivisionError:
			pass

if __name__ == '__main__':
	main()
