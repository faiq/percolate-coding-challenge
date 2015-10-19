import re

with open('data.in', 'r') as f:
	out = list()
	for line in f:
		candidate = line.rfind(',')
		last_word = line[candidate+2:] if candidate > -1 else ''
		user = dict()
		fields = line.split(',')
		if re.match('^(\d{5})$', last_word):
			# zip code format is Lastname, Firstname, (703)-742-0996, Blue, 10013
			user_keys = ['lastname', 'firstname', 'phonenumber', 'color', 'zipcode']
			for i, key in enumerate(user_keys):
				user[key] = fields[i].strip()
		elif re.match('^([a-z])', last_word):
			# color format is Firstname, Lastname, 10013, 646 111 0101, Green
			user_keys = ['firstname', 'lastname', 'zipcode', 'phonenumber', 'color']
			for i, key in enumerate(user_keys):
				user[key] = fields[i].strip()
		else:
			# phone format is Firstname Lastname, color, 10013, 646 111 0101
			if len(fields) > 1:
				sanatize_field = fields[0]
				first, last = sanatize_field[:sanatize_field.rfind(' ')], sanatize_field[sanatize_field.rfind(' ')+1:]
				user['firstname'] = first
				user['lastname'] = last
				remaining_keys = ['color', 'zipcode', 'phonenumber']
				for i in range(1, 4):
					key = remaining_keys[i-1]
					user[key] = fields[i] 
			else: 
				print 'error', fields
		print user
