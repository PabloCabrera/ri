#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import re

config = {
	"min_word_length": 3,
	"max_word_length": 40,
	"token_output_file": "terminos.txt",
	"stats_output_file": "estadisticas.txt",
	"candidate_stop_words_output_file": "candidate_stop_words.txt",
	"show_document_freq": False,
	"save_candidate_stop_words": True,
	"candidate_stop_word_ocurrency_ratio": 0.50,
}


tokens_by_file = dict ()
terms_by_file = dict ()

class Term:

	def __init__ (term, text):
		term.text = text
		term.ocurrences = dict ()

	def add_ocurrence (term, filename, update_term_counter=False):
		if (filename not in term.ocurrences):
			term.ocurrences[filename] = 1
			if (update_term_counter):
				stats["term_count"] += 1
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
	def add_term (termlist, token, filename, update_term_counter=False):
		if (token not in termlist.terms):
			termlist.terms[token] = Term (token)
		termlist.terms[token].add_ocurrence (filename, update_term_counter)


stats = {
	"document_count": 0,
	"token_count": 0,
	"term_count": 0,
	"term_character_count": 0,
	"avg_tokens_by_document": None,
	"avg_terms_by_document": None,
	"avg_term_length": None
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
	calculate_stats (stats, sys.argv[1])
	print_stats (stats)
	sys.exit (0)

def generate_term_list (dirname, stop_words):
	term_list = TermList ()
	for filename in os.listdir (dirname):
		global terms_by_file
		global tokens_by_file
		tokens_by_file[filename] = set ()
		terms_by_file[filename] = set ()
		file = open (os.path.join (dirname, filename), "r")
		for line in file:
			line_tokens = tokenizar (line)
			if (stop_words != None):
				line_tokens = sacar_palabras_vacias (line_tokens, stop_words)
			if (line_tokens is not None):
				for token in line_tokens:
					term_list.add_term (token, filename, update_term_counter=True)
					tokens_by_file[filename].add (token)
					terms_by_file[filename].add (token) #Este se va a remover si es palabra vacia
					stats["term_character_count"] += len (token)
		file.close ()
		if (stop_words != None):
			terms_by_file = sacar_palabras_vacias (terms_by_file, stop_words)
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
				stats["term_character_count"] += len(token)
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

def calculate_stats (stats, dirname):
	shortest = get_shortest_file (dirname)
	longest = get_longest_file (dirname)

	global terms_by_file
	global tokens_by_file
	stats["avg_tokens_by_document"] = (stats ["token_count"] / stats["document_count"])
	stats["avg_terms_by_document"] = (stats ["term_count"] / stats["document_count"])
	stats["avg_term_length"] = (stats["term_character_count"] / stats ["term_count"])
	stats["shortest_document_token_count"] = len (tokens_by_file[shortest])
	stats["shortest_document_term_count"] = len (terms_by_file[shortest])
	stats["longest_document_token_count"] = len (tokens_by_file[longest])
	stats["longest_document_term_count"] = len (terms_by_file[longest])

def get_shortest_file (dirname):
	shortest = None
	for filename in os.listdir (dirname):
		path = os.path.join (dirname, filename)
		if (os.path.isfile (path)) and ((shortest is None) or (os.path.getsize (path) < shortest)):
			shortest = filename
	return shortest

def get_longest_file (dirname):
	longest = None
	for filename in os.listdir (dirname):
		path = os.path.join (dirname, filename)
		if (os.path.isfile (path)) and ((longest is None) or (os.path.getsize (path) > longest)):
			longest = filename
	return longest

def print_stats (stats):
	file = open (config["stats_output_file"], "w")
	file.write ("Documentos procesados: %i%s" %(stats ["document_count"], os.linesep))
	file.write ("Tokens procesados: %i%s" %(stats ["token_count"], os.linesep))
	file.write ("Terminos procesados: %i%s" %(stats ["term_count"], os.linesep))
	file.write ("Promedio de tokens por documento: %d%s" %(stats["avg_tokens_by_document"], os.linesep))
	file.write ("Promedio de terminos por documento: %d%s" %(stats["avg_terms_by_document"], os.linesep))
	file.write ("Largo promedio de un termino: %d caracteres%s" %(stats["avg_term_length"], os.linesep))
	file.write ("Cantidad de tokens en documento mas corto: %d%s" %(stats["shortest_document_token_count"], os.linesep))
	file.write ("Cantidad de terminos en documento mas corto: %d%s" %(stats["shortest_document_term_count"], os.linesep))
	file.write ("Cantidad de tokens en documento mas largo: %d%s" %(stats["longest_document_token_count"], os.linesep))
	file.write ("Cantidad de terminos en documento mas largo: %d%s" %(stats["longest_document_term_count"], os.linesep))
	file.close ()

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
		file.write ("%s CF:%i, DF: %i%s" %(token, total, len(term.ocurrences), os.linesep))
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

