#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import re

class Term:

	def __init__ (term, text):
		term.text = text
		term.ocurrences = dict ()

	def add_ocurrence (term, filename):
		if (filename not in term.ocurrences):
			term.ocurrences[filename] = 1
		else:
			term.ocurrences[filename] += 1

	def count_ocurrences (term):
		count = 0
		for filename in term.ocurrences:
			count += term.ocurrences[filename]
		return count

class TermList:
	def __init__ (termlist):
		termlist.terms = dict ()
	def add_term (termlist, token, filename):
		if (token not in termlist.terms):
			termlist.terms[token] = Term (token)
		termlist.terms[token].add_ocurrence (filename)

config = {
	"min_word_length": 3,
	"max_word_length": 40,
	"token_output_file": "terminos.txt",
	"candidate_stop_words_output_file": "candidate_stop_words.txt",
	"show_document_freq": False,
	"save_candidate_stop_words": True,
	"candidate_stop_word_ocurrency_ratio": 0.50,
}

stats = {
	"document_count": 0,
	"token_count": 0,
	"word_count": 0,
	"min_document_length": None,
	"max_document_length": None,
	"min_token_per_document": None,
	"max_token_per_document": None
}


def main ():

	if (len (sys.argv) < 2):
		print "Uso: python tokenizar.py <directorio-corpus> [archivo-palabras-vacias]"
		exit (1)

	stop_words = None
	if (len (sys.argv) > 2):
		stop_words_filename = sys.argv[2]
		stop_words = file_get_words (stop_words_filename)

	term_list = generate_term_list (sys.argv[1], stop_words)
	generate_terminos_txt (term_list)
	process_candidate_stop_words (term_list, stats)
	print_stats (stats)
	sys.exit (0)

def generate_term_list (dirname, stop_words):
	term_list = TermList ()
	for filename in os.listdir (dirname):
		file = open (os.path.join (dirname, filename), "r")
		for line in file:
			line_tokens = tokenizar (line)
			if (stop_words != None):
				line_tokens = sacar_palabras_vacias (line_tokens, stop_words)
			if (line_tokens is not None):
				for token in line_tokens:
					term_list.add_term (token, filename)
		file.close ()
		stats["document_count"] += 1
	return term_list

	

def tokenizar (text):
	tokens = list ()
	for token in text.strip().split(" "):
		normalized_tokens = normalize_token (token)
		for token in normalized_tokens.strip().split(" "):
			if ((len (token) >= config["min_word_length"]) and (len (token) <= config["max_word_length"])):
				tokens.append (token)
				stats["token_count"] += 1
	return tokens

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

def sacar_palabras_vacias (tokens, stop_words):
	new_list = list (tokens)
	for word in stop_words:
		num_matches = new_list.count (word)
		for x in range (0, num_matches):
			new_list.remove (word)
	return new_list

def file_get_words (filename):
	words = list()
	file = open (filename, "r")
	for line in file:
		for word in line.strip().split(" "):
			words.append (word)
	return words

def print_stats (stats):
	print "Se han procesado %i documentos" %(stats ["document_count"])
	print "Se han procesado %i tokens" %(stats ["token_count"])

def generate_terminos_txt (term_list):
	filename = config["token_output_file"]
	truncate_file (filename)
	print_term_list (term_list, filename)	

def truncate_file (filename):
	file = open (filename, "w")
	file.close ()

def print_term_list (termlist, out_filename):
	file = open (out_filename, "a")
	sorted_terms = sorted (termlist.terms, reverse=True, key=lambda k: termlist.terms[k].count_ocurrences())
	for token in sorted_terms:
		term = termlist.terms[token]
		total = term.count_ocurrences ()
		file.write ("%s (%i apariciones)%s" %(token, total, os.linesep))
		if (config["show_document_freq"]):
			for in_filename in sorted (term.ocurrences, reverse=True, key=lambda k: term.ocurrences[k]):
				file.write ("\t%i %s%s" %(term.ocurrences[in_filename], in_filename, os.linesep))
	file.close ()

def process_candidate_stop_words (termlist, stats):
	if (config["save_candidate_stop_words"]):
		min_document_match = config["candidate_stop_word_ocurrency_ratio"] * stats["document_count"]
		output_filename = config["candidate_stop_words_output_file"]
		save_candidate_stop_words (termlist, min_document_match, output_filename)

def save_candidate_stop_words (termlist, min_document_match, filename):
	file = open (filename, "w")
	for key in termlist.terms:
		term = termlist.terms[key]
		count_document_match = len (term.ocurrences)
		if (count_document_match >= min_document_match):
			file.write ("%s%s" %(term.text, os.linesep))
	file.close()

if __name__ == "__main__":
	main ()

