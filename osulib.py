import requests
import json
from enum import Enum
import requests
import json
from osu.pp_calc import acc_calc

osuSTD = 0
osuTaiko = 1
osuCTB = 2
osuMania = 3

class mods(Enum):
	NoMod          = 0
	NoFail         = 1
	Easy           = 2
	TouchDevice    = 4
	Hidden         = 8
	HardRock       = 16
	SuddenDeath    = 32
	DoubleTime     = 64
	Relax          = 128
	HalfTime       = 256
	Nightcore      = 512    #// Only set along with DoubleTime. i.e: NC only gives 576
	Flashlight     = 1024
	Autoplay       = 2048
	SpunOut        = 4096
	Relax2         = 8192	#// Autopilot
	Perfect        = 16384  #// Only set along with SuddenDeath. i.e: PF only gives 16416  
	Key4           = 32768
	Key5           = 65536
	Key6           = 131072
	Key7           = 262144
	Key8           = 524288
	FadeIn         = 1048576
	Random         = 2097152
	Cinema         = 4194304
	Target         = 8388608
	Key9           = 16777216
	KeyCoop        = 33554432
	Key1           = 67108864
	Key3           = 134217728
	Key2           = 268435456
	ScoreV2        = 536870912
	LastMod        = 1073741824
	KeyMod = Key1 | Key2 | Key3 | Key4 | Key5 | Key6 | Key7 | Key8 | Key9 | KeyCoop
	FreeModAllowed = NoFail | Easy | Hidden | HardRock | SuddenDeath | Flashlight | FadeIn | Relax | Relax2 | SpunOut | KeyMod
	ScoreIncreaseMods = Hidden | HardRock | DoubleTime | Flashlight | FadeIn

class osu():
	def __init__(self, key):
		self.url = "https://osu.ppy.sh/api"
		self.naurl = "https://osu.ppy.sh"
		self.key = key

	def getRecent(self, user, mode=osuSTD):
		r = requests.get(f"{self.url}/get_user_recent?k={self.key}&u={user}&m={mode}&limit=1")
		if not r.json():
			return False
		recent = r.json()[0]
		gettitle = self._getBeatmapTitle(recent["beatmap_id"])
		title = f"{gettitle[0]} - {gettitle[1]} [{gettitle[2]}]"
		if recent['rank'] == "F":
			return dict(rank=recent["rank"], pp=0.0, x50=recent["count50"],x100=recent["count100"],
						x300=recent["count300"], misses=recent["countmiss"], bmid=recent["beatmap_id"],
						date=recent["date"], combo=recent["maxcombo"],
						maxcombo=self._getBeatmapCombo(recent["beatmap_id"]), title=title,
						mods=self._modsToString(recent["enabled_mods"]),
						acc=round(acc_calc(int(recent["count300"]), int(recent["count100"]), int(recent["count50"]), int(recent["countmiss"])) * 100, 2))
		score = self.getScores(bmid=recent["beatmap_id"], mode=mode, user=user)
		ind = 0
		if len(score) == 1:
			score[0]["title"] = title
			score[0]["bmid"] = recent["beatmap_id"]
			return score[0]
		for i in score:
			if i["date"] == recent["date"]:
				ind = score.index(i)
				break
		score[ind]["bmid"] = recent["beatmap_id"]
		score[ind]["title"] = title
		return

	def getScores(self, bmid, mode=osuSTD, user=None, limit=5):
		r = ""
		if not user:
			r = requests.get(f"{self.url}/get_scores?k={self.key}&b={bmid}&limit={limit}&m={mode}")
		else:
			r = requests.get(f"{self.url}/get_scores?k={self.key}&b={bmid}&u={user}&m={mode}&limit={limit}")
		scores = r.json()
		if not scores:
			return False
		onR = []
		for i in scores:
			onR.append(dict(rank=i["rank"], scoreID=i["score_id"], score=i["score"], x50=i["count50"],
							x100=i["count100"], x300=i["count300"], misses=i["countmiss"], pp=i["pp"],
							acc=round(acc_calc(int(i["count300"]), int(i["count100"]), int(i["count50"]), int(i["countmiss"])) * 100, 2),
							combo=i["maxcombo"], maxcombo=self._getBeatmapCombo(bmid), date=i["date"],
							mods=self._modsToString(i["enabled_mods"]), username=i["username"]))
		return onR

	def getUser(self, user, isID=False):
		r = None
		if not isID:	
			r = requests.get(f"{self.url}/get_user?k={self.key}&u={user}&type=string")
		else:
			r = requests.get(f"{self.url}/get_user?k={self.key}&u={user}&type=id")
		u = r.json()
		if not u:
			return None
		u = u[0]
		return dict(username=u["username"], id=u["user_id"], pp=u["pp_raw"], rank=u["pp_rank"],
					countryrank=u["pp_country_rank"], country=u["country"], acc=round(float(u["accuracy"]), 2) if u["accuracy"] else 0.0,
					x300=u["count300"], x100=u["count100"], x50=u["count50"], playcount=u["playcount"],
					level=u["level"], SS=u["count_rank_ss"], SSH=u["count_rank_ssh"], A=u["count_rank_a"],
					S=u["count_rank_s"], SH=u["count_rank_sh"])

	def getBeatmap(self, bmid, isset=False):
		br = None
		if not isset:
			br = requests.get(f"{self.url}/get_beatmaps?k={self.key}&b={bmid}")
		else:
			br = requests.get(f"{self.url}/get_beatmaps?k={self.key}&s={bmid}")
		map = br.json()
		if not map:
			return None
		map = map[-1]
		return dict(artist=map["artist"], title=map["title"], difficulty=map["version"],
					OD=map["diff_overall"], AR=map["diff_approach"], CS=map["diff_size"],
					maxcombo=map["max_combo"], stars=map["difficultyrating"],
					beatmapsetid=map["beatmapset_id"], beatmapid=map["beatmap_id"], status=map["approved"],
					length=map["total_length"])

	def _getBeatmapCombo(self, bmid):
		br = requests.get(f"{self.url}/get_beatmaps?k={self.key}&b={bmid}")
		return br.json()[0]["max_combo"]

	def _getBeatmapTitle(self, bmid):
		br = requests.get(f"{self.url}/get_beatmaps?k={self.key}&b={bmid}")
		map = br.json()[0]
		return map["artist"], map["title"], map["version"]

	def _getLatestScoreID(self, bmid, mode=osuSTD, user=None, limit=5):
		if not user:
			r = requests.get(f"{self.url}/get_scores?k={self.key}&b={bmid}&limit={limit}")
			scores = r.json()
			if not scores:
				return False
			scoreids = []
			for i in scores:
				print(int(i["score_id"]))
				scoreids.append(int(i["score_id"]))
			return max(scoreids)
		else:
			r = requests.get(f"{self.url}/get_scores?k={self.key}&b={bmid}&limit={limit}&u={user}")
			scores = r.json()
			if not scores:
				return False
			scoreids = []
			for i in scores:
				print(int(i["score_id"]))
				scoreids.append(int(i["score_id"]))
			return max(scoreids)

	def _modsToString(self, enumedMods):
		enumedMods = int(enumedMods)
		if enumedMods == 0:
			return "NoMod"
		if enumedMods == 1:
			return "NF"
		if enumedMods == 2:
			return "EZ"
		if enumedMods == 8:
			return "HD"
		if enumedMods == 16:
			return "HR"
		if enumedMods == 32:
			return "SD"
		if enumedMods == 64:
			return "DT"
		if enumedMods == 256:
			return "HT"
		if enumedMods == 576:
			return "NC"
		if enumedMods == 1024:
			return "FL"
		if enumedMods == 16416:
			return "PF"
		if enumedMods == 3:
			return "NFEZ"
		if enumedMods == 9:
			return "NFHD"
		if enumedMods == 10:
			return "NFEZ"
		if enumedMods == 11:
			return "NFEZHD"
		if enumedMods == 17:
			return "NFHR"
		if enumedMods == 24:
			return "HDHR"
		if enumedMods == 25:
			return "NFHDHR"
		if enumedMods == 72:
			return "HDDT"
		if enumedMods == 80:
			return "HRDT"
		if enumedMods == 88:
			return "HRHDDT"
		if enumedMods == 1048:
			return "HDHRFL"
		if enumedMods == 1080:
			return "HDHRFLSD"
		if enumedMods == 1096:
			return "HDDTFL"
		if enumedMods == 1112:
			return "HRHDDTFL"
		if enumedMods == 1144:	
			return "HDHRDTFLSD"
		if enumedMods == 1616:
			return "HRNCFL"
		if enumedMods == 1624:
			return "HDHRNCFL"
		if enumedMods == 1656:
			return "HDHRNCFLSD"
		if enumedMods == 17528:
			return "HDHRDTFLPF"
		if enumedMods == 18040:
			return "HDHRNCFLPF"
		return f"Unknown combination: {enumedMods}"

class tillerino():
	def __init__(self, key):
		self.key = key
		self.url = "https://api.tillerino.org"

	def getBeatmapFile(self, bmid):
		r = requests.get(f"{self.url}/beatmaps/byId/{bmid}/file?k={self.key}")
		if r.status_code == 200:
			return r.text
		return None

	def getBeatmapObject(self, bmid):
		r = requests.get(f"{self.url}/beatmaps/byId/{bmid}?k={self.key}")
		if r.status_code == 200:
			return r.json()
		return None

	def getBeatmapLength(self, bmid):
		r = requests.get(f"{self.url}/beatmaps/byId/{bmid}?k={self.key}")
		if r.status_code == 200:
			return r.json()["totalLength"]
		return None

	def beatmapPP(self, bmid, m=None, acc=None):
		r = ""
		if not m:
			m = mods.NoMod.value
		else:
			m = sum(self._formatMods([m[i:i+2] for i in range(0, len(m), 2)]))
			if not m:
				m = mods.NoMod.value
		if not acc:
			r = requests.get(f"{self.url}/beatmapinfo?beatmapid={bmid}&k={self.key}&mods={m}")
		else:
			r = requests.get(f"{self.url}/beatmapinfo?beatmapid={bmid}&k={self.key}&mods={m}&acc={acc/100}")
		if r.status_code == 200:
			j = r.json()
			test = False
			for i in j["ppForAcc"]["entry"]:
				if i["key"] in [0.75, 0.8, 0.85, 0.9, 0.93, 0.975, 0.985, 0.995]:
					j["ppForAcc"]["entry"].remove(i)
					test = True
			if test:
				for i in range(2):
					del j["ppForAcc"]["entry"][0]
			return [dict(acc=round(x["key"]*100, 2), pp=round(x["value"], 2)) for x in j["ppForAcc"]["entry"]]
		if r.status_code == 404:
			return False
		return None

	@staticmethod
	def _formatMods(mod:list):
		onR = []
		for m in mod:
			if m == "HR":
				onR.append(mods.HardRock.value)
				continue
			if m == "HD":
				onR.append(mods.Hidden.value)
				continue
			if m == "DT":
				onR.append(mods.DoubleTime.value)
				continue
			if m == "NC":
				onR.append(mods.Nightcore.value)
				continue
			if m == "FL":
				onR.append(mods.Flashlight.value)
				continue
			if m == "SD":
				onR.append(mods.SuddenDeath.value)
				continue
			if m == "PF":
				onR.append(mods.Perfect.value)
				continue
			if m == "EZ":
				onR.append(mods.Easy.value)
				continue
			if m == "HT":
				onR.append(mods.HalfTime.value)
				continue
			if m == "NF":
				onR.append(mods.NoFail.value)
				continue
			if m == "SO":
				onR.append(mods.SpunOut.value)
				continue

		if len(onR) == 1:
			if onR[0] == "PF":
				onR[0] = mods.Perfect.value + mods.SuddenDeath.value
			if onR[0] == "NC":
				onR[0] = mods.Nightcore.value + mods.DoubleTime.value
		return onR


if __name__ == '__main__':
	pass
