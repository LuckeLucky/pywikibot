import sys

import random
import string
import importlib
import pywikibot

COMMONS = 'commons'

def generateId():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 10))
	return ran

def importClass(language: str, attributeName: str):
	if not language:
		pywikibot.stdout("<<lightred>>Language is empty.")
		sys.exit(1)

	classFound = None
	try:
		module = importlib.import_module(f'scripts.match2.{language}.{attributeName.lower()}')
		classFound = getattr(module, attributeName, lambda: None)
	except ModuleNotFoundError:
		classFound = None

	if classFound is None:
		language = COMMONS
		module = importlib.import_module(f'scripts.match2.{attributeName.lower()}')
		classFound = getattr(module, attributeName, lambda: None)
		pywikibot.info('Using Default '+ attributeName)

	if hasattr(classFound, 'language'):
		setattr(classFound, 'language', language)
	return classFound