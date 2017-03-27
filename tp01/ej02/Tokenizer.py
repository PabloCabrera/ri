#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from ConfigParser import ConfigParser

class Tokenizer:
	def __init__ (tokenizer, config):
		tokenizer.config = config
		tokenizer.load_entities_file ("entities.json")

	def tokenize (tokenizer, text):
		tokens = list ()
		for token in text.strip().split(" "):
			normalized_tokens = tokenizer.normalize_token (token)
			for token in normalized_tokens.strip().split(" "):
				tokens.append (token)
		return tokens

	def remove_stop_words (tokenizer, tokens, stop_words):
		# Es necesario hacer una copia para no eliminar elementos de la lista sobre la que estamos iterando
		copy_tokens = list (tokens)
		for token in copy_tokens:
			if token in stop_words:
				tokens.remove (token)
		return tokens

	def remove_invalid_length_words (tokenizer, tokens):
		min_len = int (tokenizer.config.get("Tokenizer", "min_word_length"))
		max_len = int (tokenizer.config.get("Tokenizer", "max_word_length"))

		copy_tokens = list (tokens)
		for token in copy_tokens:
			if ((len (token) < min_len) or (len (token) > max_len)):
				tokens.remove (token)
		return tokens

	def normalize_token (tokenizer, text):
		text = re.sub (u"[^0-9a-záéíóúÅÉÍÓÚñ]+", "", text)
		text = re.sub ("^[0-9]+$", "", text) # quitamos numeros si estan solos
		if tokenizer.config.getboolean("Tokenizer", "replace_weird_characters"):
			token = tokenizer.replace_weird_characters (text.lower())
		else:
			token = text.lower()
		return token

	def replace_weird_characters (tokenizer, text):
		tabin = u'áéíóúÅÉÍÓÚñ'
		tabout = u'aeiouaeioun'
		token = tokenizer.translate (text, tabin, tabout)
		return token

	def translate (tokenizer, to_translate, tabin, tabout):
		tabin = [ord (char) for char in tabin]
		translate_table = dict (zip (tabin, tabout))
		return to_translate.translate (translate_table)

	def load_entities_file (tokenizer, filename):
		file = open (filename)
		tokenizer.entity_desc = json.load (file)
		file.close ()

	def get_entities (tokenizer, text):
		found_list = None
		for entity_type in tokenizer.entity_desc:
			search_text = text
			while len (search_text) > 0:
				result = re.search (tokenizer.entity_desc[entity_type], search_text)
				if result is not None:
					startpos = result.start ()
					endpos = result.end()
					entity = search_text[startpos:endpos]
					if (found_list is None):
						found_list = list ()
					found_list.append (entity.strip (" ,.;-"))
					search_text = search_text[endpos:]
				else:
					search_text = ""
		return found_list;

	if __name__ == "__main__":
		Ej02 (sys.argv)

