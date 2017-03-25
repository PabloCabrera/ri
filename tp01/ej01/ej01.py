#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import re
from Collection import *
from Document import *
from TokenInCollection import *
from TokenInDocument import *
from CollectionPrinter import *
from config import config

class Ej01:
	def __init__ (ej01, args):
		if (len (args) < 2):
			print "Uso: python tokenizar.py <directorio-corpus> [archivo-palabras-vacias]"
			sys.exit (1)

		input_dir = args[1]
		stop_words = ej01.get_stop_words (args)

		collection = Collection ()
		ej01.add_documentdir_collection (input_dir, collection, stop_words)
		ej01.print_collection (collection)
		sys.exit (0)

	def get_stop_words (ej01, args):
		stop_words = None
		if (len (args) > 2):
			stop_words_filename = sys.argv[2]
			stop_words = ej01.file_get_words (stop_words_filename)
		return stop_words

	def file_get_words (ej01, filename):
		words = list()
		file = open (filename, "r")
		for line in file:
			for word in line.strip().split(" "):
				words.append (word)
		return words

	def add_documentdir_collection (ej01, dirname, collection, stop_words=None):
		for filename in os.listdir (dirname):
			file = open (os.path.join (dirname, filename), "r")
			for line in file:
				tokens = tokenizar (line)
				if (stop_words is None):
					terms = list (tokens)
				else:
					terms = sacar_palabras_vacias (tokens, stop_words)

				collection.add_token_list (tokens, filename)
				collection.add_term_list (terms, filename)
			file.close ()

	def print_collection (ej01, collection):
		printer = CollectionPrinter (collection)
		printer.print_terms ("terminos.txt")
		printer.print_statistics ("estadisticas.txt")
		printer.print_top_ten ("top_ten.txt")

def tokenizar (text):
	tokens = list ()
	for token in text.strip().split(" "):
		normalized_tokens = normalize_token (token)
		for token in normalized_tokens.strip().split(" "):
			if ((len (token) >= config["min_word_length"]) and (len (token) <= config["max_word_length"])):
				tokens.append (token)
	return tokens

def sacar_palabras_vacias (tokens, stop_words):
	new_list = list (tokens)
	for token in tokens:
		if token in stop_words:
			new_list.remove (token)
	return new_list

def normalize_token (text):
	regex="[!\"$%&/()=?\\|@#\[\]{}.:,;]+"
	if (re.search (regex, text) is not None):
		token = re.sub (regex, " ", text)
	else:
		token = text
	#token = replace_weird_characters (text)
	return token.lower()

def replace_weird_characters (text):
	tabin = u'áéíóú'
	tabout = u'aeiou'
	token = translate (text, tabin, tabout)
	return token

def translate (to_translate, tabin, tabout):
	to_translate = to_translate.decode('utf-8')
	tabin = [ord(char) for char in tabin]
	translate_table = dict(zip(tabin, tabout))
	return to_translate.translate(translate_table).encode('utf-8')


if __name__ == "__main__":
	Ej01 (sys.argv)

