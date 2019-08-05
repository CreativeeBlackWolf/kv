import urllib.request, urllib.error
import vk_api
import time
import json
import requests
import sys
import os
import shutil
import zipfile
from lxml import html

try:
	from beatmap import Beatmap
	import pp_calc
	import diff_calc
except ModuleNotFoundError:
	from osu.beatmap import Beatmap
	import osu.pp_calc as pp_calc
	import osu.diff_calc as diff_calc

def calcMap(t = None, beatmap = None, c50 = 0, c100 = 0, amods = None, combo = 0, acc = 0.0, sv = 1, misses = 0, uid = 0, messageid = 0):
	vk_session = vk_api.VkApi(token=t)
	vk = vk_session.get_api()

	if not beatmap.startswith("https://"):
		beatmap = f"https://{beatmap}"

	ch = requests.get(beatmap, allow_redirects=True)
	beatmap = ch.url

	bmid = 0
	diffid = 0
	file = ""
	diff = ""
	map = None
	ex = True

	if len(beatmap.split("/")) == 6:
		bmid = beatmap.split("/")[-2].split("#")[0]
		diffid = beatmap.split("/")[-1]
	if len(beatmap.split("/")) == 5:
		bmid = beatmap.split("/")[-1]

	r = requests.get(beatmap)
	tree = html.fromstring(r.text)
	parse = tree.xpath('//script[@id="json-beatmapset"]')[0]
	beatmapinfo = json.loads(parse.text)
	for d in beatmapinfo["beatmaps"]:
		if diffid:
			if str(d["id"]) == str(diffid):
				diff = "".join(c for c in d["version"] if c not in '?:!/&;*')
				break
	if not diff:
		diff = "".join(c for c in beatmapinfo["beatmaps"][-1]['version'] if c not in '?:!/&;*')

	beatmapinfo["title"] = "".join(c for c in beatmapinfo["title"] if c not in '?:!/&;*')
	beatmapinfo["artist"] = "".join(c for c in beatmapinfo["artist"] if c not in '?:!/&;*')

	dir = f"Beatmap-{bmid}"

	if __name__ == '__main__':
		ex = os.path.exists(os.path.join("tmp", "dotosu", dir))
	else:
		ex = os.path.exists(os.path.join("osu", "tmp", "dotosu", dir))

	if not ex:
		url = ""
		try:
			print("connecting ripple...")
			urllib.request.urlopen(f"https://storage.ripple.moe/d/{bmid}")
		except urllib.error.HTTPError:	
			print("ripple storage 404/406")
		else:
			url = f"https://storage.ripple.moe/d/{bmid}"
		if not url:
			try:
				print("connecting bloodcat...")
				x = urllib.request.urlopen(f'https://bloodcat.com/osu/s/{bmid}')
				if "* File not found or inaccessible!" in str(x.read()):
					raise Exception
			except urllib.error.HTTPError:
				print("bloodcat storage error")
				return "Can't connect to all the mirrors"
			except Exception:
				print("bloodcat storage error")
				return "Can't connect to all the mirrors"
			else:
				url = f"https://bloodcat.com/osu/s/{bmid}"
		try:
			if __name__ == '__main__':
				os.mkdir(f"tmp\\dotosu\\Beatmap-{beatmapinfo['id']}")
				urllib.request.urlretrieve(url, os.path.join("tmp", f"{beatmapinfo['artist']} - {beatmapinfo['title']}.zip"), reporthook)
				urllib.request.urlretrieve(beatmapinfo['covers']['cover@2x'], f"tmp\\dotosu\\{dir}\\thumbnail.jpg")
			else:
				os.mkdir(f"osu\\tmp\\dotosu\\Beatmap-{beatmapinfo['id']}")
				vk.messages.edit(peer_id=uid, message_id=messageid, message="Downloading beatmap file...")
				urllib.request.urlretrieve(url, os.path.join("osu", "tmp", f"{beatmapinfo['artist']} - {beatmapinfo['title']}.zip"), reporthook)				
				urllib.request.urlretrieve(beatmapinfo['covers']['cover@2x'], f"osu\\tmp\\dotosu\\{dir}\\thumbnail.jpg")

		except Exception as e:
			if __name__ == '__main__':
				if ex:
					os.remove(os.path.join("tmp", f"{beatmapinfo['artist']} - {beatmapinfo['title']}.zip"))
					shutil.rmtree(os.path.join("tmp", "dotosu", dir))
			else:
				if ex:
					os.remove(os.path.join("osu", "tmp", f"{beatmapinfo['artist']} - {beatmapinfo['title']}.zip"))
					shutil.rmtree(os.path.join("osu", "tmp", "dotosu", dir))
			print(e)
			return "\nUnexpected error when downloading map"

		if __name__ == '__main__':
			arch = zipfile.ZipFile(os.path.join("tmp", f"{beatmapinfo['artist']} - {beatmapinfo['title']}.zip"))
		else:
			arch = zipfile.ZipFile(os.path.join("osu", "tmp", f"{beatmapinfo['artist']} - {beatmapinfo['title']}.zip"))
		for i in arch.namelist():
			if i.endswith(f".osu"):
				if __name__ == '__main__':
					arch.extract(i, os.path.join("tmp", "dotosu", dir))
					os.rename(
							os.path.join("tmp", "dotosu", dir, i),
							os.path.join("tmp", "dotosu", dir, f"{bmid}[{''.join(c for c in i.split('[')[1][:-5:] if c not in '?:!/&;*')}].osu")
							)
				else:
					vk.messages.edit(peer_id=uid, message_id=messageid, message=f"Unpacking {i}")
					arch.extract(i, os.path.join("osu", "tmp", "dotosu", dir))
					os.rename(
							os.path.join("osu", "tmp", "dotosu", dir, i),
							os.path.join("osu", "tmp", "dotosu", dir, f"{bmid}[{''.join(c for c in i.split('[')[1][:-5:] if c not in '?:!/&;*')}].osu")
							)
	if __name__ == '__main__':
		map = Beatmap(open(os.path.join("tmp", "dotosu", dir, f"{bmid}[{diff}].osu"), encoding="utf-8"))
	else:
		map = Beatmap(open(os.path.join("osu", "tmp", "dotosu", dir, f"{bmid}[{diff}].osu"), encoding="utf-8"))

	if combo <= 0 or combo > map.max_combo:
		combo = map.max_combo

	def mod_str(mod):
		string = ""
		if mod.nf:
			string += "NF"
		if mod.ez:
			string += "EZ"
		if mod.hd:
			string += "HD"
		if mod.hr:
			string += "HR"
		if mod.dt:
			string += "DT"
		if mod.ht:
			string += "HT"
		if mod.nc:
			string += "NC"
		if mod.fl:
			string += "FL"
		if mod.so:
			string += "SO"
		if mod.td:
			string += "TD"
		return string

	class mods:
		def __init__(self):
			self.nomod = 0,
			self.nf = 0
			self.ez = 0
			self.hd = 0
			self.hr = 0
			self.dt = 0
			self.ht = 0
			self.nc = 0
			self.fl = 0
			self.so = 0
			self.td = 0
			self.speed_changing = self.dt | self.ht | self.nc
			self.map_changing = self.hr | self.ez | self.speed_changing
		def update(self):
			self.speed_changing = self.dt | self.ht | self.nc
			self.map_changing = self.hr | self.ez | self.speed_changing
	
	mod = mods()

	def set_mods(mod, m):
		if m == "NF":
			mod.nf = 1
		if m == "EZ":
			mod.ez = 1
		if m == "HD":
			mod.hd = 1
		if m == "HR":
			mod.hr = 1
		if m == "DT":
			mod.dt = 1
		if m == "HT":
			mod.ht = 1
		if m == "NC":
			mod.nc = 1
		if m == "FL":
			mod.fl = 1
		if m == "SO":
			mod.so = 1
		if m == "TD":
			mod.td = 1

	if amods:
		amods = amods.upper()
		amods = [amods[i:i+2] for i in range(0, len(amods), 2)]
		for m in amods:
			set_mods(mod, m)
			mod.update()

	mod_string = mod_str(mod)
	map.apply_mods(mod)
	diff = diff_calc.main(map)
	pa = []
	if not acc:
		for i in range(95, 101):
			pp = pp_calc.pp_calc_acc(diff[0], diff[1], diff[3], i, mod, combo, misses, sv)
			pa.append(round(pp.pp, 2))
	else:
		pp = pp_calc.pp_calc_acc(diff[0], diff[1], diff[3], acc, mod, combo, misses, sv)
		pa.append(round(pp.pp, 2))
	pp.pp += 0.7
	title = f"{map.artist} - {map.title} [{map.version}] by {map.creator}"
	if mod_string:
		title += f" ({mod_string})"
	else:
		title += " (NoMod)"

	if __name__ != '__main__':
		vk.messages.edit(peer_id=uid, message_id=messageid, message="Done")
	return {"title": title, "AR": round(map.ar, 2), "CS": round(map.cs, 2), "OD": round(map.od, 2), 
	"aim": round(diff[0], 2), "speed": round(diff[1], 2), "stars": round(diff[2], 2), 
	"acc": round(pp.acc_percent, 2), "combo": combo, "maxcombo": map.max_combo,
	"PP": pa, "beatmapid": bmid, "mods": mod_string}

def calcMapNoDownload(beatmap = None, c50 = 0, c100 = 0, amods = None, combo = 0, acc = 0.0, sv = 1, misses = 0):
	map = Beatmap(open("temp.osu"))

	if combo <= 0 or combo > map.max_combo:
		combo = map.max_combo

	def mod_str(mod):
		string = ""
		if mod.nf:
			string += "NF"
		if mod.ez:
			string += "EZ"
		if mod.hd:
			string += "HD"
		if mod.hr:
			string += "HR"
		if mod.dt:
			string += "DT"
		if mod.ht:
			string += "HT"
		if mod.nc:
			string += "NC"
		if mod.fl:
			string += "FL"
		if mod.so:
			string += "SO"
		if mod.td:
			string += "TD"
		return string

	class mods:
		def __init__(self):
			self.nomod = 0,
			self.nf = 0
			self.ez = 0
			self.hd = 0
			self.hr = 0
			self.dt = 0
			self.ht = 0
			self.nc = 0
			self.fl = 0
			self.so = 0
			self.td = 0
			self.speed_changing = self.dt | self.ht | self.nc
			self.map_changing = self.hr | self.ez | self.speed_changing
		def update(self):
			self.speed_changing = self.dt | self.ht | self.nc
			self.map_changing = self.hr | self.ez | self.speed_changing
	
	mod = mods()

	def set_mods(mod, m):
		if m == "NF":
			mod.nf = 1
		if m == "EZ":
			mod.ez = 1
		if m == "HD":
			mod.hd = 1
		if m == "HR":
			mod.hr = 1
		if m == "DT":
			mod.dt = 1
		if m == "HT":
			mod.ht = 1
		if m == "NC":
			mod.nc = 1
		if m == "FL":
			mod.fl = 1
		if m == "SO":
			mod.so = 1
		if m == "TD":
			mod.td = 1

	if amods:
		amods = amods.upper()
		amods = [amods[i:i+2] for i in range(0, len(amods), 2)]
		for m in amods:
			set_mods(mod, m)
			mod.update()

	mod_string = mod_str(mod)
	map.apply_mods(mod)
	diff = diff_calc.main(map)
	pa = []
	if not acc:
		for i in range(95, 101):
			pp = pp_calc.pp_calc_acc(diff[0], diff[1], diff[3], i, mod, combo, misses, sv)
			pa.append(round(pp.pp, 2))
	else:
		pp = pp_calc.pp_calc_acc(diff[0], diff[1], diff[3], acc, mod, combo, misses, sv)
		pa.append(round(pp.pp, 2))
	pp.pp += 0.7
	title = f"{map.artist} - {map.title} [{map.version}] by {map.creator}"
	if mod_string:
		title += f" ({mod_string})"
	else:
		title += " (NoMod)"

	return {"title": title, "AR": round(map.ar, 2), "CS": round(map.cs, 2), "OD": round(map.od, 2), 
	"aim": round(diff[0], 2), "speed": round(diff[1], 2), "stars": round(diff[2], 2), 
	"acc": round(pp.acc_percent, 2), "combo": combo, "maxcombo": map.max_combo,
	"PP": pa, "mods": mod_string}

def reporthook(blocknum, blocksize, totalsize):
	readsofar = blocknum * blocksize
	if totalsize > 0:
		percent = readsofar * 1e2 / totalsize
		s = "\r%5.1f%% %*d / %d" % (
			percent, len(str(totalsize)), readsofar, totalsize)
		sys.stderr.write(s)
		if readsofar >= totalsize: # near the end
			sys.stderr.write("\n")
	else: # total size is unknown
		sys.stderr.write("read %d\n" % (readsofar,))

if __name__ == "__main__":
	pass
