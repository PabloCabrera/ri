#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import io
import fileinput
from ConfigParser import ConfigParser
from Tokenizer import *
from TokenInCollection import *
from TokenInDocument import *
from Stemmer import *
from InvertedIndex import *

class Indexer:
	def __init__ (self, args):
		if (len (args) < 2):
			print "Uso: python self.py <directorio-corpus> [archivo-palabras-vacias]"
			sys.exit (1)

		input_dir = args[1]
		stop_words = self.get_stop_words (args)
		self.config = self.load_config_file ("config.ini")
		self.tokenizer = Tokenizer (self.config)
		self.stemmer = Stemmer (self.config)
		self.documents = dict ()
		self.invertedIndex = InvertedIndex ()

		print "Generando índice de búsqueda ..."
		self.add_documentdir (input_dir, stop_words)
		print "Escribiendo archivo de índice..."
		self.lexicon = self.write_index_file ("index.bin")
		self.write_lexicon ("lexicon.txt")
		self.write_documents_index ("documents.txt")

	def get_stop_words (self, args):
		stop_words = None
		if (len (args) > 2):
			stop_words_filename = sys.argv[2]
			stop_words = self.file_get_words (stop_words_filename)
		return stop_words

	def file_get_words (self, filename):
		words = list()
		file = io.open (filename, mode="r", encoding="UTF-8")
		for line in file:
			for word in line.strip().split(" "):
				words.append (word)
		return words

	def load_config_file (self, filename):
		global CONFIG
		CONFIG = ConfigParser ()
		CONFIG.read (filename)
		return CONFIG

	def add_documentdir (self, dirname, stop_words=None):
		procesados = 0
		doc_id = 0;
		for filename in os.listdir (dirname):
			doc_id += 1
			document = {"name": filename, "doc_id": doc_id}
			self.documents[filename] = document
			file = io.open (os.path.join (dirname, filename), mode="r", encoding="UTF-8")
			for line in file:
				self.add_line_terms_to_index (line, stop_words, document)
			file.close ()
			procesados +=1
			print "Documentos procesados: %d" % procesados

	def add_line_terms_to_index (self, line, stop_words, document):
		try:
			terms = self.tokenizer.tokenize (line)

			if (stop_words is not None):
				terms = self.tokenizer.remove_stop_words (terms, stop_words)
				terms = self.tokenizer.remove_invalid_length_words (terms)

			stemmed_terms = self.stemmer.stem (terms)

			for term in stemmed_terms:
				self.invertedIndex.add (term, document)

		except UnicodeDecodeError:
			print "WARNING: %s no utiliza codificacion UTF-8." % filename

	def write_index_file (self, filename):
		lexicon = self.invertedIndex.store (filename)
		return lexicon

	def write_lexicon (self, filename):
		output = open (filename, "w")
		for term in self.lexicon:
			output.write ("%s: %d %d\n" % (term, self.lexicon[term]["df"], self.lexicon[term]["position"]))
		output.close

	def write_documents_index (self, filename):
		output = open (filename, "w")
		for name in self.documents:
			output.write ("%d %s\n" % (self.documents[name]["doc_id"], name))
		output.close

	def show_lexicon (self):
		for term in self.lexicon:
			print ("[%s] df: %d, position: %d" % (term, self.lexicon[term]["df"], self.lexicon[term]["position"]))


if __name__ == "__main__":
	Indexer (sys.argv)

