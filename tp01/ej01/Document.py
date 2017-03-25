from TokenInDocument import *

class Document:

	def __init__ (document, name):
		document.name = name
		document.terms = dict ()
		document.tokens = dict ()

	def get_token_count (document):
		num_tokens = 0
		for key in document.tokens:
			num_tokens += document.tokens[key].frequency
		return num_tokens

	def get_term_count (document):
		return len (document.terms)

	def add_token_list (document, token_list):
		for token in token_list:
			document.add_token_ocurrency (token)

	def add_token_ocurrency (document, token):
		if token in document.tokens:
			document.tokens[token].frequency += 1
		else:
			document.tokens[token] = TokenInDocument (token)
	
	def add_term_list (document, term_list):
		for term in term_list:
			document.add_term_ocurrency (term)

	def add_term_ocurrency (document, term):
		if term in document.terms:
			document.terms[term].frequency += 1
		else:
			document.terms[term] = TokenInDocument (term)

