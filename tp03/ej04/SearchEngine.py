#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct
import time
from collections import OrderedDict
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

	def load_config_file (engine, filename):
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
			plen = int (numbers[0])
			position = int (numbers[1])
			engine.lexicon[term] = {"plen": plen, "position": position}
		lexicon_file.close ()

	def start_interactive_search (engine):
		closeness = int (engine.config.get ("SearchEngine", "near_operator_closeness"))
		print ("Ingrese una consulta")
		print ("Operador por defecto: proximidad (%d)" % closeness)
		print ("Escriba una consulta entre comillas dobles (\"...\") para búsqueda por frases");
		exit = False
		while not exit:
			line = raw_input ("BUSCAR> ").decode ("utf-8")
			if (line == "") or (line == "exit"):
				exit = True
			else:
				terms = engine.tokenizer.tokenize (line)
				started_at = time.time()
				if (line[0] == '"'):
					results = engine.search_literal (terms)
				else:
					results = engine.search (terms)
				ended_at = time.time()
				engine.print_results (results, ended_at - started_at)
 
 	def search (engine, words):
		query_results = None
		closeness = int (engine.config.get ("SearchEngine", "near_operator_closeness"))
		for word in words:
			word_results = engine.get_posting (word)
			query_results = engine.join_near_results (query_results, word_results, closeness)
		return query_results

 	def search_literal (engine, words):
		query_results = dict()
		for word in words:
			word_results = engine.get_posting (word)
			query_results = engine.join_consecutive_results (query_results, word_results)
		return query_results

	def get_posting (engine, term):
		posting = None
		if (term in engine.lexicon):
			plen = engine.lexicon[term]["plen"]
			position = engine.lexicon[term]["position"]
			engine.index.seek (position*4)
			bytes_readed = engine.index.read (plen*4)
			int_array = struct.unpack ("%dI" % plen, bytes_readed)
			posting = engine.unpack_posting (int_array)
		else:
			print "Ignorando %s (no esta en vocabulario)" % term
		return posting

	def unpack_posting (engine, int_array):
		processed = 0
		posting = OrderedDict ();
		while (processed < len (int_array)):
			doc_id = int_array [processed]
			frequency = int_array [processed+1]
			processed += 2
			posting[doc_id] = dict()
			posting[doc_id] = int_array[processed:processed+frequency]
			processed += frequency
		return posting

	def join_near_results (engine, res1, res2, closeness):
		# Unir resultados para busquedas por proximidad
		if res1 is None:
			return res2
		elif res2 is None:
			return res1

		res_joined = OrderedDict()
		for doc_id in res1:
			if doc_id in res2:
				if engine.min_diff (res1[doc_id], res2[doc_id]) <= closeness:
					res_joined[doc_id] = engine.join_near_ocurrences (res1[doc_id], res2[doc_id], closeness)
		if len (res_joined) > 0:
			return res_joined
		else:
			return None

	def min_diff (engine, list1, list2):
		# Devuelve la distancia minima entre los elementos de list1 y list2
		# Usado para comparar filtrar resultados en busquedas por proximidad
		actual_min = abs (list1[0] - list2[0])
		for w1 in list1:
			for w2 in list2:
				dif = abs(w1 - w2)
				if dif < actual_min:
					actual_min = dif
		return actual_min

	def join_near_ocurrences (engine, list1, list2, closeness):
		# Unir ocurrencias para busquedas por proximidad
		joined = []
		for w1 in list1:
			for w2 in list2:
				if abs(w1 - w2) <= closeness:
					joined.append (w1)
					joined.append (w2)
		return joined

	def join_consecutive_results (engine, res1, res2):
		# Unir resultados para busquedas por frases

		if res1 is None or res2 is None:
			return None
		if len(res1) == 0:
			return res2
		if len(res2) == 0:
			return res1


		res_joined = OrderedDict()
		for doc_id in res1:
			if doc_id in res2:
				oc_joined = engine.join_consecutive_ocurrences (res1[doc_id], res2[doc_id])
				if len (oc_joined) > 0:
					res_joined[doc_id] = oc_joined
		if len (res_joined) > 0:
			return res_joined
		else:
			return None

	def join_consecutive_ocurrences (engine, list1, list2):
		# Unir ocurrencias para busquedas por frases

		joined = []
		for w1 in list1:
			for w2 in list2:
				if w1 +1 == w2:
					joined.append (w2)
		return joined

		pass

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

