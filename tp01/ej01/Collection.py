from TokenInCollection import *
from Document import *

class Collection:
	def __init__ (collection):
		collection.documents = dict ()
		collection.terms = dict ()
		collection.tokens = dict ()

	def get_terms_sorted_by_freq (collection):
		sorted_list = list ()
		sorted_keys = sorted (collection.terms, reverse=True, key=lambda k: collection.terms[k].cf)
		for key in sorted_keys:
			sorted_list.append (collection.terms[key])
		return sorted_list

	def get_document_count (collection):
		return len (collection.documents)

	def get_token_count (collection):
		num_token = 0
		for key in collection.tokens:
			num_token += collection.tokens[key].cf
		return num_token

	def get_term_count (collection):
		return len (collection.terms)

	def get_avg_tokens_per_document (collection):
		avg = 0
		num_documents = len (collection.documents)
		if num_documents > 0:
			total = 0
			for key in collection.documents:
				document = collection.documents[key]
				total += document.get_token_count ()
			avg = total / num_documents
		return avg

	def get_avg_terms_per_document (collection):
		avg = 0
		num_documents = len (collection.documents)
		if num_documents > 0:
			total = 0
			for key in collection.documents:
				document = collection.documents[key]
				total += document.get_term_count ()
			avg = total / num_documents
		return avg

	def get_avg_term_length (collection):
		avg = 0
		num_terms = len (collection.terms)
		if num_terms > 0:
			total = 0
			for term in collection.terms:
				total += len (term)
			avg = total / num_terms
		return avg

	def get_shortest_document (collection):
		min_tokens = None
		shortest = None
		for key in collection.documents:
			document = collection.documents[key]
			num_tokens = document.get_token_count ()
			if (shortest == None) or (num_tokens < min_tokens):
				shortest = document
				min_tokens = num_tokens
		return shortest

	def get_longest_document (collection):
		max_tokens = None
		longest = None
		for key in collection.documents:
			document = collection.documents[key]
			num_tokens = document.get_token_count ()
			if (longest == None) or (num_tokens > max_tokens):
				longest = document
				max_tokens = num_tokens
		return longest

	def get_hapax (collection):
		hapaxi = dict ()
		for key in collection.terms:
			term = collection.terms[key]
			if (term.cf == 1):
				hapaxi[key] = term
		return hapaxi

	def get_top_freq_terms (collection, num_terms):
		term_list = list ()
		sorted_terms_str = sorted (collection.terms, reverse=True, key=lambda k: collection.terms[k].cf)
		for key in sorted_terms_str[:num_terms]:
			term_list.append (collection.terms[key])
		return term_list

	def get_bottom_freq_terms (collection, num_terms):
		term_list = list ()
		sorted_terms_str = sorted (collection.terms, key=lambda k: collection.terms[k].cf)
		for key in sorted_terms_str[:num_terms]:
			term_list.append (collection.terms[key])
		return term_list

	def add_token_list (collection, token_list, documentname):
		for token in token_list:
			if token in collection.tokens:
				collection.tokens[token].cf += 1
				if documentname not in collection.tokens[token].documents:
					collection.tokens[token].documents.add (documentname) 
					collection.tokens[token].df += 1
			else:
				collection.tokens[token] = TokenInCollection (token)
				collection.tokens[token].documents.add (documentname) 

		if documentname not in collection.documents:
			document = Document (documentname)
			collection.documents[documentname] = document
		collection.documents[documentname].add_token_list (token_list)

	def add_term_list (collection, term_list, documentname):
		for term in term_list:
			if term in collection.terms:
				collection.terms[term].cf += 1
				if documentname not in collection.terms[term].documents:
					collection.terms[term].documents.add (documentname) 
					collection.terms[term].df += 1
			else:
				collection.terms[term] = TokenInCollection (term)
				collection.terms[term].documents.add (documentname) 

		if documentname not in collection.documents:
			document = Document (documentname)
			collection.documents[documentname] = document
		collection.documents[documentname].add_term_list (term_list)

