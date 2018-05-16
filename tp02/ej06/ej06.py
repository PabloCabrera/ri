#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import io
import fileinput
from ConfigParser import ConfigParser
from Tokenizer import *
from Collection import *
from Document import *
from Stemmer import *

class Ej06:
	def __init__ (ej06, args):
		if (len (args) < 2):
			print "Uso: python ej06.py <directorio-corpus> [archivo-palabras-vacias]"
			sys.exit (1)

		input_dir = args[1]
		stop_words = ej06.get_stop_words (args)
		ej06.config = ej06.load_config_file ("config.ini")
		ej06.tokenizer = Tokenizer (ej06.config)
		ej06.stemmer = Stemmer (ej06.config)

		ej06.collection = Collection ()
		print "Generando índice de búsqueda ..."
		ej06.add_documentdir_collection (input_dir, ej06.collection, stop_words)
		ej06.start_interactive_search ()
		sys.exit (0)

	def get_stop_words (ej06, args):
		stop_words = None
		if (len (args) > 2):
			stop_words_filename = sys.argv[2]
			stop_words = ej06.file_get_words (stop_words_filename)
		return stop_words

	def file_get_words (ej06, filename):
		words = list()
		file = io.open (filename, mode="r", encoding="UTF-8")
		for line in file:
			for word in line.strip().split(" "):
				words.append (word)
		return words

	def load_config_file (ej06, filename):
		global CONFIG
		CONFIG = ConfigParser ()
		CONFIG.read (filename)
		return CONFIG

	def add_documentdir_collection (ej06, dirname, collection, stop_words=None):
		procesados = 0
		for filename in os.listdir (dirname):
			file = io.open (os.path.join (dirname, filename), mode="r", encoding="UTF-8")
			try:
				for line in file:
					tokens = ej06.tokenizer.tokenize (line)
					terms = list (tokens)

					if (stop_words is not None):
						terms = ej06.tokenizer.remove_stop_words (terms, stop_words)
					terms = ej06.tokenizer.remove_invalid_length_words (terms)
					stemmed_terms = ej06.stemmer.stem (terms)

					collection.add_term_list (stemmed_terms, filename)
			except UnicodeDecodeError:
				print "WARNING: %s no utiliza codificacion UTF-8. Se aborta el procesamiento de dicho documento." % filename
			file.close ()
			procesados +=1
			print "Documentos procesados: %d" % procesados

	def start_interactive_search (ej06):
		exit = False
		while (not exit):
			line = raw_input ("\nBUSCAR> ").decode ("utf-8");
			if (line == ""):
				exit = True;
			else:
				# words = line.split(" ")
				words = ej06.tokenizer.tokenize (line)
				stemmed = ej06.stemmer.stem (words)
				results = ej06.collection.search (stemmed)
				if (len (results) > 0):
					position = 1
					for result in results:
						print "[%d] %s (%.3f)" % (position, result["document"].name, result["score"])
						position += 1
				else:
					print "No se han encontrado resultados"

if __name__ == "__main__":
	Ej06 (sys.argv)

