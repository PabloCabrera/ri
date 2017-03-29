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
from CollectionDrawer import *

class Ej05:
	def __init__ (ej05, args):
		if (len (args) < 2):
			print "Uso: python ej05.py <directorio-corpus> [archivo-palabras-vacias]"
			sys.exit (1)

		input_dir = args[1]
		stop_words = ej05.get_stop_words (args)
		ej05.config = ej05.load_config_file ("config.ini")
		ej05.tokenizer = Tokenizer (ej05.config)

		collection = Collection ()
		ej05.add_documentdir_collection (input_dir, collection, stop_words)
		ej05.print_collection (collection)
		ej05.draw_images (collection)
		sys.exit (0)

	def get_stop_words (ej05, args):
		stop_words = None
		if (len (args) > 2):
			stop_words_filename = sys.argv[2]
			stop_words = ej05.file_get_words (stop_words_filename)
		return stop_words

	def file_get_words (ej05, filename):
		words = list()
		file = io.open (filename, mode="r", encoding="UTF-8")
		for line in file:
			for word in line.strip().split(" "):
				words.append (word)
		return words

	def load_config_file (ej05, filename):
		global CONFIG
		CONFIG = ConfigParser ()
		CONFIG.read (filename)
		return CONFIG

	def add_documentdir_collection (ej05, dirname, collection, stop_words=None):
		for filename in os.listdir (dirname):
			file = io.open (os.path.join (dirname, filename), mode="r", encoding="UTF-8")
			try:
				for line in file:
					entities = ej05.tokenizer.get_entities (line)
					if entities is None:
						tokens = ej05.tokenizer.tokenize (line)
					else:
						rest_of_line = ej05.remove_entities (line, entities)
						tokens = ej05.tokenizer.tokenize (rest_of_line)
						tokens.extend (entities)

					terms = list (tokens)

					if (stop_words is not None):
						terms = ej05.tokenizer.remove_stop_words (terms, stop_words)
					terms = ej05.tokenizer.remove_invalid_length_words (terms)

					collection.add_token_list (tokens, filename)
					collection.add_term_list (terms, filename)
			except UnicodeDecodeError:
				print "WARNING: %s no utiliza codificacion UTF-8. Se aborta el procesamiento de dicho documento." % filename
			file.close ()

	def remove_entities (ej05, text, entities):
		newstr = text
		for entity in entities:
			newstr = newstr.replace (entity, "")
		return newstr

	def print_collection (ej05, collection):
		global CONFIG
		printer = CollectionPrinter (collection)
		printer.print_terms (CONFIG.get ("Paths", "terms_file"))
		printer.print_statistics (CONFIG.get ("Paths", "statistics_file"))
		printer.print_top_ten (CONFIG.get ("Paths", "top_file"))

	def draw_images (ej05, collection):
		drawer = CollectionDrawer (collection)
		drawer.draw ();

if __name__ == "__main__":
	Ej05 (sys.argv)

