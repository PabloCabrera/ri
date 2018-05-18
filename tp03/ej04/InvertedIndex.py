#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import json
from collections import OrderedDict

class InvertedIndex:
	def __init__ (self):
		self.index = OrderedDict ()
	
	def add (self, term, doc_id, term_pos):
		if (term in self.index):
			if doc_id in self.index[term]:
				self.index[term][doc_id].append (term_pos)
			else:
				self.index[term][doc_id] = [term_pos]
		else:
			self.index[term] = OrderedDict()
			self.index[term][doc_id] = [term_pos]


	def get (self, term):
		if (term in self.index):
			return self.index[term]
		else:
			return []

	def getDF (self, term):
		return len (self.get (term))
	
	def store (self, filename):
		# Formato del archivo binario:
		# doc_id,freq,pos1,pos2..posN;doc_id,freq,pos1,pos2..posN
		lexicon = dict ()
		filestore = open (filename, "w")
		sum_plen = 0
		for term in self.index:
			bin_data = ""
			plen = 0
			df = len (self.index [term])
			for doc_id in self.index [term]:
				ocurrences = self.index[term][doc_id]
				num_ocurrences = len (ocurrences)
				quantifier = "%dI" % (2+num_ocurrences)
				bin_data += struct.pack (quantifier, doc_id, num_ocurrences, *ocurrences)
				plen += 2 + num_ocurrences
			filestore.write ("%s" % bin_data)
			lexicon[term] = {"term": term, "plen": plen, "position": sum_plen}
			sum_plen += plen
		filestore.close ()
		return lexicon
	
	def writeJson (self, filename):
		with open(filename, 'w') as outfile:
			json.dump(self.index, outfile, indent=4, separators=(',', ': '))

