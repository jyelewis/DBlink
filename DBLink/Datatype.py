import cgi

class DatatypeBase():
	def viewHTML(self, value):
		if value is not None:
			return cgi.escape(str(value))
		else:
			return ''