#!/usr/bin/env python

import sys
import math
import time
import struct
from Tokenizer import *
from ConfigParser import *

class SearchEngine:

	def __init__ (engine, lexicon_file,  documents_file, index_file):
		engine.config = engine.load_config_file ("config.ini")
		engine.tokenizer = Tokenizer (engine.config)
		engine.index = open (index_file, "r")
		print "Cargando archivo documentos ..."
		engine.load_documents (documents_file)
		print "Cargando Lexicon"
		engine.load_lexicon (lexicon_file)
		engine.start_interactive_search ()

	def __del__ (engine):
		engine.index.close ()

	def load_config_file (self, filename):
		global CONFIG
		CONFIG = ConfigParser ()
		CONFIG.read (filename)
		return CONFIG

	def load_documents (engine, filename):
		engine.documents = dict ()
		docs_file = open (filename, "r")
		for line in docs_file:
			words = line.split (" ")
			doc_id = int (words.pop (0))
			doc_name = " ".join (words).strip()
			engine.documents [doc_id] = doc_name
		docs_file.close ()

	def load_lexicon (engine, filename):
		engine.lexicon = dict()
		lexicon_file = open (filename, "r")
		for line in lexicon_file:
			pieces = line.split (":")
			term = pieces[0]
			numbers = pieces[1].strip().split (" ")
			df = int (numbers[0])
			position = int (numbers[1])
			engine.lexicon[term] = {"df": df, "position": position}
		lexicon_file.close ()

	def start_interactive_search (engine):
		exit = False
		while not exit:
			line = raw_input ("BUSCAR> ").decode ("utf-8")
			if (line == "") or (line == "exit"):
				exit = True
			else:
				terms = engine.tokenizer.tokenize (line)
				started_at = time.time()
				relevants = engine.get_relevant_documents (terms)
				ranking = engine.rank_relevant_documents (relevants, terms)
				ended_at = time.time()
				engine.show_ranking (ranking, ended_at - started_at)
 
 	def get_relevant_documents (engine, query_terms):
		relevants = dict()
		weighting = engine.config.get("SearchEngine", "weighting")
		for term in query_terms:
			relevants[term] = engine.get_posting (term, weighting)
		return relevants

	def rank_relevant_documents (engine, relevants, query_terms):
		if relevants is None:
			return []
		temp = dict()
		for term in relevants:
			if relevants[term] is not None:
				for doc_id in relevants[term]:
					if doc_id not in temp:
						temp[doc_id] = []
					temp[doc_id].append (relevants[term][doc_id])

		ranking = []
		for doc_id in temp:
			ranking.append ({"doc_id": doc_id, "weight": engine.euclidean_dist (temp[doc_id])})
		ranking = sorted (ranking, key=lambda(x):x["weight"], reverse=True)

		# Hacer lo que sea necesario
		return ranking

	def euclidean_dist (engine, elems):
		sq_sum = 0
		for elem in elems:
			sq_sum += math.pow (elem, 2)
		return math.sqrt (sq_sum)

	def show_ranking (engine, ranking, elapsed):
		rank = 1
		for document in ranking:
			print "[%d] %s (%f)" %(rank, engine.documents[document["doc_id"]], document["weight"])
			rank += 1
		print "Respuesta obtenida en %f segundos" % elapsed
		
	def show_ranking_2 (engine, ranking, elapsed):
		for term in ranking:
			print "Relevantes para termino %s:" % term
			for document in ranking[term]:
				print "  doc_id: %d, weight: %f" % (document, ranking[term][document])
			print ""
			
		print ""
		print "Respuesta obtenida en %f segundos" % elapsed
		
	def get_posting (engine, term, weighting):
		result = None
		if (term in engine.lexicon):
			df = engine.lexicon[term]["df"]
			position = engine.lexicon[term]["position"]
			engine.index.seek (position)

			# Leemos 4 campos de 4 Bytes cada uno: doc_id, tf, rtf, tf_idf
			bytes_readed = engine.index.read (df*16)
			val_array = struct.unpack ("Ifff" * df, bytes_readed)
			result = dict()

			for i in range (0, len (val_array)/4):
				doc_id = val_array[4*i]
				tf = val_array[4*i+1]
				rtf = val_array[4*i+2]
				tf_idf = val_array[4*i+3]

				if weighting == "tf":
					result[doc_id] = tf
				elif weighting == "rtf":
					result[doc_id] = rtf
				elif weighting == "tf_idf":
					result[doc_id] = tf_idf
				else:
					raise ValueError ("Esquema de pesos (" + weighting + ") no valido")
		else:
			print "Ignorando %s (no esta en vocabulario)" % term

		return result

	def print_results (engine, results, elapsed):
		print (results)
		if results is not None:
			for doc_id in results:
				print engine.documents[doc_id]
		if elapsed is not None:
			print ""
			print "Respuesta obtenida en %f segundos" % elapsed

if __name__ == "__main__":
	if len (sys.argv) == 4:
		SearchEngine (sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print "Uso: python SearchEngine.py <archivo-lexicon> <archivo-documentos> <archivo-posting-lists>"
		sys.exit (1)

