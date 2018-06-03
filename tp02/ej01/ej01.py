#!/usr/bin/env python

import math

def main ():
	inverted_index = load_inverted_index ("ejemploRibeiro/documentVector.txt")
	direct_index = load_direct_index ("ejemploRibeiro/documentVector.txt")
	queries = load_direct_index ("ejemploRibeiro/queries.txt")

	for num_query in queries:
		print "Query %d" % num_query
		query = queries [num_query]
		result_bool_and = eval_boolean_and (query, inverted_index)
		result_bool_or = eval_boolean_or (query, inverted_index)
		result_vectorial = eval_vectorial (query, inverted_index, direct_index)
		print "Modelo Booleano AND:"
		print_search_result (result_bool_and)
		print "Modelo Booleano OR:"
		print_search_result (result_bool_or)
		print "Modelo Vectorial:"
		print_search_result (result_vectorial)
		print ""


def load_inverted_index (filename):
	index = {}
	file_in = open (filename, "r")
	for line in file_in:
		parts = line.split (" ")
		if len (parts) > 2:
			doc_id = int (parts[1].replace(":", ""))
			for i in range (2, len(parts)):
				term_id = int (parts[i].replace("(", "").replace(",", "").replace(")", "").replace("\n", ""))
				if (term_id not in index):
					index[term_id] = []
				index[term_id].append(doc_id)
	file_in.close()
	return index

def load_direct_index (filename):
	queries = {}
	file_in = open (filename, "r")
	for line in file_in:
		parts = line.split (" ")
		if len (parts) > 2:
			query_id = int (parts[1].replace(":", ""))
			queries[query_id] = []
			for i in range (2, len(parts)):
				doc_id = int (parts[i].replace("(", "").replace(",", "").replace(")", "").replace("\n", ""))
				queries[query_id].append (doc_id)
	return queries
	
def eval_boolean_and (query, inverted_index):
	relevants = None
	scores = []

	for term_id in query:
		if term_id in inverted_index:
			retrieved = inverted_index[term_id][:]
			if relevants is None:
				relevants = retrieved[:]
			else:
				for term_relevant in relevants:
					if term_relevant not in retrieved:
						relevants.remove (term_relevant)
		else:
			return []

	for doc_id in relevants:
		scores.append ((doc_id, 1))

	return scores


def eval_boolean_or (query, inverted_index):
	relevants = None
	scores = []

	for term_id in query:
		if term_id in inverted_index:
			retrieved = inverted_index[term_id][:]
			if relevants is None:
				relevants = retrieved[:]
			else:
				for term_retrieved in retrieved:
					if term_retrieved not in relevants:
						relevants.append (term_retrieved)

	for doc_id in relevants:
		scores.append ((doc_id, 1))
	
	return scores

def eval_vectorial (query, inverted_index, direct_index):
	relevants = []
	scores = []

	for term in query:
		if (term in query):
			if term in inverted_index:
				retrieved = inverted_index[term]
				for doc in retrieved:
					if doc not in relevants:
						relevants.append (doc)

	for doc in relevants:
		doc_full = direct_index[doc]
		similarity = get_similarity (query, doc_full)
		scores.append ((doc, similarity))

	result = sorted (scores, key = (lambda x: x[1]), reverse = True)

	return result

def get_similarity (query, doc_full):
	vector1 = []
	vector2 = []

	query_norm = math.sqrt (len (query))
	doc_norm = math.sqrt (len (doc_full))

	for term in query:
		vector1.append (1)
		if term in doc_full:
			vector2.append(1)
		else:
			vector2.append(0)
	return cos_sim (vector1, vector2, query_norm, doc_norm)

def cos_sim (vector1, vector2, query_norm, doc_norm):
	value = 0
	squaresum = 0
	for i in range(0, len(vector1)):
		value += vector1[i] * vector2[i]
	
	value = value / (query_norm * doc_norm)

	return value
	
def print_search_result (scores):
	if len (scores) > 0:
		ranking = 1
		for element in scores:
			print "\t[%d] Doc %d  (%.4f)" % (ranking, element[0], element[1])
			ranking += 1
	else:
		print "No hay resultados"

main ()

