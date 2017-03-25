#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import re
from ConfigParser import ConfigParser
from Collection import *
from Document import *
from TokenInCollection import *
from TokenInDocument import *
from CollectionPrinter import *

class Ej01:
	def __init__ (ej01, args):
		if (len (args) < 2):
			print "Uso: python tokenizar.py <directorio-corpus> [archivo-palabras-vacias]"
			sys.exit (1)

		input_dir = args[1]
		stop_words = ej01.get_stop_words (args)
		ej01.load_config_file ("config.ini")

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

	def load_config_file (ej01, filename):
		global CONFIG
		CONFIG = ConfigParser ()
		CONFIG.read (filename)

	def add_documentdir_collection (ej01, dirname, collection, stop_words=None):
		for filename in os.listdir (dirname):
			file = open (os.path.join (dirname, filename), "r")
			for line in file:
				tokens = tokenizar (line)
				terms = list (tokens)

				if (stop_words is not None):
					terms = sacar_palabras_vacias (terms, stop_words)
				terms = sacar_palabras_largo_invalido (terms)

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
			tokens.append (token)
	return tokens

def sacar_palabras_vacias (tokens, stop_words):
	# Es necesario hacer una copia para no eliminar elementos de la lista sobre la que estamos iterando
	copy_tokens = list (tokens)
	for token in copy_tokens:
		if token in stop_words:
			tokens.remove (token)
	return tokens

def sacar_palabras_largo_invalido (tokens):
	global CONFIG
	min_len = int (CONFIG.get("Tokenizer", "min_word_length"))
	max_len = int (CONFIG.get("Tokenizer", "max_word_length"))

	copy_tokens = list (tokens)
	for token in copy_tokens:
		if ((len (token) < min_len) or (len (token) > max_len)):
			tokens.remove (token)
	return tokens

def normalize_token (text):
	token = replace_weird_characters (text.lower())
	return token

def replace_weird_characters (text):
	tabin = u'áéíóúÅÉÍÓÚñ'
	tabout = u'aeiouaeioun'
	token = translate (text, tabin, tabout)
	token = re.sub ("[^0-9a-z]+", "", token)
	token = re.sub ("^[0-9]+$", "", token) # quitamos numeros si estan solos
	return token

def translate (to_translate, tabin, tabout):
	to_translate = to_translate.decode('utf-8')
	tabin = [ord(char) for char in tabin]
	translate_table = dict(zip(tabin, tabout))
	return to_translate.translate(translate_table).encode('utf-8')

if __name__ == "__main__":
	Ej01 (sys.argv)

