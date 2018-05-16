#!/usr/bin/env python
# -*- coding: utf-8 -*-

class InvertedIndex:
	def __init__ (self):
		self.index = dict ()
	
	def add (self, term, document):
		if ( term in self.index):
			if document not in self.index[term]:
				self.index[term].append (document)
		else:
			self.index[term] = [document]

	def get (self, term):
		if (term in self.index):
			return self.index[term]
		else:
			return []

	def getDF (self, term):
		return len (self.get (term))
