import sys

import random
import string
import importlib
import pywikibot

def generateId():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 10))
	return ran

def getMatchGroupForLanguage(language: str, matchGroupName: str):
	if not language:
		pywikibot.stdout("<<lightred>>Language is empty.")
		sys.exit(1)

	matchGroup = None
	try:
		module = importlib.import_module(f'scripts.match2.{language}.{matchGroupName.lower()}')
		matchGroup =  getattr(module, matchGroupName, lambda: None)
	except ModuleNotFoundError:
		matchGroup = None

	if matchGroup is None:
		pywikibot.stdout(f"<<lightred>>Missing Support for {matchGroupName} in {language}.")
		sys.exit(1)
	return matchGroup
