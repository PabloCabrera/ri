#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct

class InvertedIndex:
	def __init__ (self):
		self.index = dict ()
	
	def add (self, term, document):
		if (term in self.index):
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
	
	def store (self, filename):
		lexicon = dict ()
		filestore = open (filename, "w")
		sum_df = 0
		for term in self.index:
			bin_data = ""
			df = len (self.index [term])
			for document in self.index [term]:
				bin_data += struct.pack ("I", document["doc_id"])
			filestore.write ("%s" % bin_data)
			lexicon[term] = {"term": term, "df": df, "position": sum_df}
			sum_df += df
		filestore.close ()
		return lexicon

