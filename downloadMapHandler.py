import random

import requests
import json

import tornado.gen
import tornado.web

from common.web import requestsManager
from common.sentry import sentry
from objects import glob

MODULE_NAME = "direct_download"
class handler(requestsManager.asyncRequestHandler):
	"""
	Handler for /d/
	"""
	@tornado.web.asynchronous
	@tornado.gen.engine
	@sentry.captureTornado
	def asyncGet(self, bid):
		try:
			noVideo = bid.endswith("n")
			if noVideo:
				bid = bid[:-1]
			bid = int(bid)
			requestIP = requestsManager.getRequestIP(self)
			ipa = requests.get("http://ip-api.com/json/{}?fields=continent,country".format(requestIP)).text
			jsonOut = json.loads(ipa)
			"""
			if jsonOut["continent"] == "North America" or jsonOut["continent"] == "South America":
				mirror = "https://aoba-proxy-us.herokuapp.com"
				try:
					c_mirror = "https://aoba-proxy-us.herokuapp.com"
					requests.get(c_mirror)
					print("US SERVER OK")
					response = requests.get(c_mirror+"/d/1")
					if response.status_code == 200:
						print("US DOWNLOAD WORKS")
					else:
						print("US SERVER IS DYING INSIDE, REDIRECTING TO MAIN SERVER")
						mirror = "https://storage.ainu.pw"
				except requests.exceptions.ConnectionError:
					print("US SERVER DOWN, REDIRECTING TO MAIN SERVER")
					mirror = "https://storage.ainu.pw"
			elif jsonOut["continent"] == "Europe" or jsonOut["continent"] == "Africa":
				eu_mirror = ['https://storage.ainu.pw', 'https://aoba-proxy-eu.herokuapp.com']
				try:
					c_mirror = "https://aoba-proxy-eu.herokuapp.com"
					requests.get(c_mirror)
					print("EU SERVER OK")
					response = requests.get(c_mirror+"/d/1")
					if response.status_code == 200:
						print("EU DOWNLOAD WORKS")
						eu_mirror = ['https://storage.ainu.pw', 'https://aoba-proxy-eu.herokuapp.com']
						mirror = random.choice(eu_mirror)
					else:
						print("EU SERVER IS DYING INSIDE, REDIRECTING TO MAIN SERVER")
						mirror = "https://storage.ainu.pw"
				except requests.exceptions.ConnectionError:
					print("EU SERVER DOWN, REDIRECTING TO MAIN SERVER")
					mirror = "https://storage.ainu.pw"
			elif jsonOut["continent"] == "Australia":
				mirror = "https://bm.realm.so"
				try:
					c_mirror = "https://bm.realm.so"
					requests.get(c_mirror)
					print("AU SERVER OK")
					response = requests.get(c_mirror+"/d/1")
					if response.status_code == 200:
						print("AU DOWNLOAD WORKS")
					else:
						print("AU SERVER IS DYING INSIDE, REDIRECTING TO MAIN SERVER")
						mirror = "https://storage.ainu.pw"
				except requests.exceptions.ConnectionError:
					print("AU SERVER DOWN, REDIRECTING TO MAIN SERVER")
					mirror = "https://storage.ainu.pw"
			# Server is too slow, so I disabled it.
#			elif jsonOut["continent"] == "Asia":
#				mirror = "https://bm-th.ainu.pw"
#				try:
#					c_mirror = "https://bm-th.ainu.pw"
#					requests.get(c_mirror)
#					print("TH/SEA SERVER OK")
#					response = requests.get(c_mirror+"/d/1")
#					if response.status_code == 200:
#						print("TH/SEA DOWNLOAD WORKS")
#					else:
#						print("TH/SEA SERVER IS DYING INSIDE, REDIRECTING TO MAIN SERVER")
#						mirror = "https://storage.ainu.pw"
#				except requests.exceptions.ConnectionError:
#					print("TH/SEA SERVER DOWN, REDIRECTING TO MAIN SERVER")
#					mirror = "https://storage.ainu.pw"
			else:
			"""
			mirror = "https://storage.rina.place"

			self.set_status(302, "Moved Temporarily")
			self.add_header("Location", "{}/d/{}{}".format(mirror, bid, "n" if noVideo else ""))
			self.add_header("Cache-Control", "no-cache")
			self.add_header("Pragma", "no-cache")
		except ValueError:
			self.set_status(400)
			self.write("Invalid set id")