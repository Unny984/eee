from urllib.parse import urlencode

import requests
import tornado.gen
import tornado.web

from constants import exceptions
from common.ripple import userUtils
from common.log import logUtils as log
from common.web import requestsManager

MODULE_NAME = "direct_np"
class handler(requestsManager.asyncRequestHandler):
	"""
	Handler for /web/osu-search-set.php
	"""
	@tornado.web.asynchronous
	@tornado.gen.engine
	def asyncGet(self):
		args = {}
		try:
			# Pass all arguments otherwise it doesn't work
			for key, _ in self.request.arguments.items():
				args[key] = self.get_argument(key)

			response = requests.get("http://127.0.0.1:32767/web/osu-search-set.php?{}".format(urlencode(args)))
			self.write(response.text)
		except Exception as e:
			log.error("search failed: {}".format(e))
			self.write("")
