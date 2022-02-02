from urllib.parse import urlencode

import requests
import tornado.gen
import tornado.web

from constants import exceptions
from common.ripple import userUtils
from common.log import logUtils as log
from common.web import requestsManager

MODULE_NAME = "direct"
class handler(requestsManager.asyncRequestHandler):
	"""
	Handler for /web/osu-search.php
	"""
	@tornado.web.asynchronous
	@tornado.gen.engine
	def asyncGet(self):
		try:
			args = {}
			try:
				# Get arguments
				gameMode = self.get_argument("m", None)
				if gameMode is not None:
					gameMode = int(gameMode)
				if gameMode < 0 or gameMode > 3:
					gameMode = None

				rankedStatus = self.get_argument("r", None)
				if rankedStatus is not None:
					rankedStatus = int(rankedStatus)

				query = self.get_argument("q", "")
				page = int(self.get_argument("p", "0"))
				if query.lower() in ["newest", "top rated", "most played"]:
					query = ""
			except ValueError:
				raise exceptions.invalidArgumentsException(MODULE_NAME)

			# Pass all arguments otherwise it doesn't work
			for key, _ in self.request.arguments.items():
				args[key] = self.get_argument(key)

			# Get data from cheesegull API
			log.info("someone has requested osu!direct search: {}".format(query if query != "" else "index"))

			response = requests.get("http://127.0.0.1:32767/web/osu-search.php?{}".format(urlencode(args)))
			self.write(response.text)
		except Exception as e:
			log.error("search failed: {}".format(e))
			self.write("")
