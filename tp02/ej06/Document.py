from TokenInDocument import *

class Document:

	def __init__ (document, name):
		document.name = name
		document.terms = dict ()

	def get_term_count (document):
		return len (document.terms)

	def add_term_list (document, term_list):
		for term in term_list:
			document.add_term_ocurrency (term)

	def add_term_ocurrency (document, term):
		if term in document.terms:
			document.terms[term].frequency += 1
		else:
			document.terms[term] = TokenInDocument (term)

