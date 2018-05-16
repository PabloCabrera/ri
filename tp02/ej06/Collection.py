from Document import *
from InvertedIndex import *
from TokenInCollection import *
import math

class Collection:
	def __init__ (collection):
		collection.documents = dict ()
		collection.invertedIndex = InvertedIndex ()
		collection.terms = dict ()

	def add_term_list (collection, term_list, documentname):

		if documentname not in collection.documents:
			document = Document (documentname)
			collection.documents[documentname] = document
		else:
			document = collection.documents[documentname]

		for term in term_list:
			collection.invertedIndex.add (term, document)
			if term in collection.terms:
				collection.terms[term].cf += 1
				if documentname not in collection.terms[term].documents:
					collection.terms[term].documents.add (documentname) 
					collection.terms[term].df += 1
			else:
				collection.terms[term] = TokenInCollection (term)
				collection.terms[term].documents.add (documentname) 

		document.add_term_list (term_list)

	def search (collection, query_terms):
		# query_words = query.split (" ")
		relevants = []
		for term in query_terms:
			relevants.extend (collection.invertedIndex.get (term))
		relevants_set = set (relevants)
		return collection.rank (relevants_set, query_terms)
	
	def rank (collection, documents, query_terms):
		n = len (collection.documents)
		scores = []
		for document in documents:
			score = 0
			# print "%s:" % (document.name)
			sum_tf2 = 0
			for term in query_terms:
				if term in document.terms:
					df = collection.invertedIndex.getDF (term)
					tf = document.terms[term].frequency
					tf2 += pow (tf, 2)
					# idf = math.log (1 + n/df)
					idf = 1 + math.log (n/df)
					tf_idf = tf * idf
					score += tf_idf * 1 # El 1 representa la cantidad de veces que aparece el termino en la query
					# Esto va a iterar tantas veces como repeticiones haya, por lo que el resultado va a ser correcto
					# print ("    %s: TF=%d, IDF=%.3f, TF_IDF=%.3f" % (term, tf, idf, tf_idf))
			score = score / (sum_tf2 * len (query_terms)) # REVISAR
			scores.append ({"document": document, "score": score})
		ranking = sorted (scores, key=lambda (elem): elem["score"], reverse=True)
		position = 1
		for element in ranking:
			position += 1
		return ranking

