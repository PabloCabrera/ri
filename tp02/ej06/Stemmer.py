# -*- coding: utf-8 -*-
from nltk.stem.snowball import SnowballStemmer

class Stemmer:
	def __init__ (stemmer, config):
		stemmer.config = config
		stemmer.enabled = config.getboolean ("Stemmer", "enabled");
		if (stemmer.enabled):
			stemmer.language = config.get ("Stemmer", "language");
			stemmer.snowball = SnowballStemmer (stemmer.language)

	def stem (stemmer, term_list):
		if (stemmer.enabled):
			stemmed = list ()
			for term in term_list:
				stemmed.append (stemmer.snowball.stem (term))
			return stemmed
		else:
			return term_list

