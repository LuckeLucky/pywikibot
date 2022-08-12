import random
import string

def generate_id():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
	return ran