class Priority(object):
	"""
	Enumerate the possible choice of priority
	"""
	low = 'Low'
	medium = 'Medium'
	high = 'High'

class Table(object):
	"""
	Table represent the name of each table in the database
	"""
	to_do = 'to_do'

class ToDo(object):
	"""
	ToDo represent a to do item, each public fields is a column in the table
	"""
	id = 'id'
	task = 'task'
	email = 'email'
	priority = 'priority'

	def __init__(self, todo):
		print(todo)
		self.id, self.priority, self.email, self.task = todo

def get_columns(obj, exclude = []):
	props = (name for name in dir(obj) if not name.startswith('_'))
	res = []
	for name in props:
		attr = getattr(obj, name)
		if type(attr).__name__ != 'function' and attr not in exclude:
			res.append(attr)
	return res
