#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import io
from ConfigParser import ConfigParser
from Tokenizer import *
from Collection import *
from Document import *
from TokenInCollection import *
from TokenInDocument import *
from CollectionPrinter import *
from Stemmer import *

class Ej04:
	def __init__ (ej04, args):
		if (len (args) < 2):
			print "Uso: python ej04.py <directorio-corpus> [archivo-palabras-vacias]"
			sys.exit (1)

		input_dir = args[1]
		stop_words = ej04.get_stop_words (args)
		ej04.config = ej04.load_config_file ("config.ini")
		ej04.tokenizer = Tokenizer (ej04.config)
		ej04.stemmer = Stemmer (ej04.config)

		collection = Collection ()
		ej04.add_documentdir_collection (input_dir, collection, stop_words)
		ej04.print_collection (collection)
		sys.exit (0)

	def get_stop_words (ej04, args):
		stop_words = None
		if (len (args) > 2):
			stop_words_filename = sys.argv[2]
			stop_words = ej04.file_get_words (stop_words_filename)
		return stop_words

	def file_get_words (ej04, filename):
		words = list()
		file = io.open (filename, mode="r", encoding="UTF-8")
		for line in file:
			for word in line.strip().split(" "):
				words.append (word)
		return words

	def load_config_file (ej04, filename):
		global CONFIG
		CONFIG = ConfigParser ()
		CONFIG.read (filename)
		return CONFIG

	def add_documentdir_collection (ej04, dirname, collection, stop_words=None):
		stem_log = io.open ("stemming.log", mode="w", encoding="UTF-8")
		for filename in os.listdir (dirname):
			file = io.open (os.path.join (dirname, filename), mode="r", encoding="UTF-8")
			try:
				for line in file:
					tokens = ej04.tokenizer.tokenize (line)
					terms = list (tokens)

					if (stop_words is not None):
						terms = ej04.tokenizer.remove_stop_words (terms, stop_words)
					terms = ej04.tokenizer.remove_invalid_length_words (terms)
					stemmed_terms = ej04.stemmer.stem (terms)

					ej04.log_stem (stem_log, terms, stemmed_terms)
					collection.add_token_list (tokens, filename)
					collection.add_term_list (stemmed_terms, filename)
			except UnicodeDecodeError:
				print "WARNING: %s no utiliza codificacion UTF-8. Se aborta el procesamiento de dicho documento." % filename
			file.close ()
		stem_log.close ()

	def log_stem (ej04, file, terms, stemmed_terms):
		index = 0
		while index < len (terms):
			file.write (u"%s => %s%s" %(terms[index], stemmed_terms[index], os.linesep))
			index += 1

	def print_collection (ej04, collection):
		global CONFIG
		printer = CollectionPrinter (collection)
		printer.print_terms (CONFIG.get ("Paths", "terms_file"))
		printer.print_statistics (CONFIG.get ("Paths", "statistics_file"))
		printer.print_top_ten (CONFIG.get ("Paths", "top_file"))

if __name__ == "__main__":
	Ej04 (sys.argv)

