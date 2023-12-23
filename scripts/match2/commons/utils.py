import random
import string

def generateId():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
	return ran
