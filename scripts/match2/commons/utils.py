import random
import string

def generateId():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 10))
	return ran
