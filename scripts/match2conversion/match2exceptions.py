class VodX(Exception):
	"""Raised when parameter like vodX or Xvod appears"""
	pass

class WikiStyle(Exception):
	"""Raised when a value as wiki style like [,],' """

class MalformedScore(Exception):
	"""Raised when score doesn't follow the format X-Y"""