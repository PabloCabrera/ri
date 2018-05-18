#!/usr/bin/env python

import sys
import struct
import time
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
				results = engine.search (terms)
				ended_at = time.time()
				engine.print_results (results, ended_at - started_at)
 
 	def search (engine, words):
		# AND es el operador por defecto, podemos ignorarlo
		while "and" in words: 
			words.remove ("and")

		# Si hay un OR, separamos las listas y las procesamos por separado
		if "or" in words:
			or_position = words.index ("or")
			res_1 = engine.search (words[0:or_position])
			res_2 = engine.search (words[or_position+1:])
			return engine.union_results (res_1, res_2)
		elif "not" in words:
			not_position = words.index ("not")
			res_inc = engine.search (words[0:not_position])
			res_exc = engine.search (words[not_position+1:])
			return engine.diff_results (res_inc, res_exc)
		else:
			query_results = ()
			for word in words:
				word_results = engine.get_posting (word)
				query_results = engine.intersection_results (query_results, word_results)
			return query_results

	def union_results (engine, res_1, res_2):
		if (res_1 == () or res_1 is None):
			return res_2
		elif (res_2 == () or res_2 is None):
			return res_1
		else:
			results = []
			results.extend (res_1)
			for entry in res_2:
				if entry not in results:
					results.append (entry)
			return results

	def intersection_results (engine, res_1, res_2):
		if (res_1 == () or res_1 is None):
			return res_2
		elif (res_2 == () or res_2 is None):
			return res_1
		else:
			results = []
			for entry in res_1:
				if entry in res_2:
					results.append (entry)
			return results

	def diff_results (engine, positive, negative):
		results = []
		for entry in positive:
			if entry not in negative:
				results.append (entry)
		return results

	def get_posting (engine, term):
		result = None
		if (term in engine.lexicon):
			df = engine.lexicon[term]["df"]
			position = engine.lexicon[term]["position"]
			engine.index.seek (position*4)
			bytes_readed = engine.index.read (df*4)
			result = struct.unpack ("%dI" % df, bytes_readed)
		else:
			print "Ignorando %s (no esta en vocabulario)" % term
		return result

	def print_results (engine, results, elapsed):
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

