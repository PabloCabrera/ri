# -*- coding: utf-8 -*-
from nltk.stem.snowball import SnowballStemmer

class Stemmer:
	def __init__ (stemmer, config):
		stemmer.config = config
		stemmer.snowball = SnowballStemmer ("spanish")

	def stem (stemmer, term_list):
		stemmed = list ()
		for term in term_list:
			stemmed.append (stemmer.snowball.stem (term))
		return stemmed

