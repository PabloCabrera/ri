class TokenInCollection:
	def __init__ (token, name):
		token.name = name
		token.cf = 1
		token.df = 1
		token.documents = set ()
