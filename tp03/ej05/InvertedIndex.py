#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import struct
from collections import OrderedDict
from ConfigParser import ConfigParser

class InvertedIndex:
	def __init__ (self):
		self.index = dict ()
		self.config = self.load_config_file ("config.ini")
	
	def add (self, term, doc_id):
		if (term in self.index):
			if doc_id not in self.index[term]:
				self.index[term][doc_id] = 1
			else:
				self.index[term][doc_id] += 1
				
		else:
			self.index[term] = OrderedDict()
			self.index[term][doc_id] = 1

	def get (self, term):
		if (term in self.index):
			return self.index[term]
		else:
			return []

	def getDF (self, term):
		return len (self.get (term))
	
	def store (self, filename, doc_lens):
		# Formato del archivo:
		# doc_id, tf; doc_id, tf; doc_id, tf
		lexicon = dict ()
		filestore = open (filename, "w")
		sum_plen = 0
		lexicon_size = len(self.index)
		for term in self.index:
			bin_data = ""
			df = len (self.index [term])
			for doc_id in self.index [term]:
				tf = self.index[term][doc_id]
				rtf = float(tf) / doc_lens[doc_id]
				tf_idf = self.tf_idf (tf, df, lexicon_size)
				bin_data += struct.pack ("Ifff", doc_id, tf, rtf, tf_idf)
			filestore.write ("%s" % bin_data)
			lexicon[term] = {"term": term, "df": df, "position": sum_plen}
			sum_plen += 16 * df # 16 corresponde a 4 campos de 4 Bytes cada uno: doc_id, tf, rtf, tf_idf
		filestore.close ()
		return lexicon
	
	def tf_idf (self, tf, df, N):
		scheme = self.config.get("Index", "tf_idf_scheme")

		if (scheme == "1"):
			result =  tf * math.log (float(N)/df)
		elif (scheme == "2"):
			result = 1 + math.log (tf)
		elif (scheme == "3"):
			result = (1 + math.log (tf)) * math.log (float(N)/df)
		else:
			raise ValueError ("Esquema de tf_idf (" + scheme + ") no valido")

		# print ("tf_idf (%d, %d, %d) = %f" % (tf, df, N, result)) # print para debug
		return result

	def load_config_file (self, filename):
		global CONFIG
		CONFIG = ConfigParser ()
		CONFIG.read (filename)
		return CONFIG

	

