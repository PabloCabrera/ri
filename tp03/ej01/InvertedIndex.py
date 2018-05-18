#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct

class InvertedIndex:
	def __init__ (self):
		self.index = dict ()
	
	def add (self, term, doc_id):
		if (term in self.index):
			if doc_id not in self.index[term]:
				self.index[term].append (doc_id)
		else:
			self.index[term] = [doc_id]

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
			for doc_id in self.index [term]:
				bin_data += struct.pack ("I", doc_id)
			filestore.write ("%s" % bin_data)
			lexicon[term] = {"term": term, "df": df, "position": sum_df}
			sum_df += df
		filestore.close ()
		return lexicon

