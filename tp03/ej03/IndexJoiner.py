import struct
from collections import OrderedDict

class IndexJoiner:

	def join (self, partial_indexes, partial_lexicons, output_index):
		output = open (output_index, "w")
		full_lexicon = OrderedDict()
		bin_files = self.open_bin_files (partial_indexes)
		print ("Obteniendo terminos")
		terms = self.get_terms (partial_lexicons)
		sum_df = 0
		print ("Generando indice completo")
		for term in terms:
			doc_ids = self.get_doc_ids (term, bin_files, partial_lexicons)
			df = len (doc_ids)
			full_lexicon[term] = {"term": term, "df": df, "position": sum_df}
			binary_doc_ids = struct.pack ("%dI" % df, *doc_ids);
			output.write (binary_doc_ids)
			sum_df += df
		output.close()
		self.close_bin_files (bin_files)
		return full_lexicon
			

	def get_terms (self, lexicons):
		terms = set ()
		for lexicon in lexicons:
			for term in lexicon:
				terms.add (term)
		return terms

	def get_doc_ids (self, term, bin_files, lexicons):
		doc_ids = []
		for i in xrange (0, len (bin_files)):
			if (term in lexicons[i]):
				lex_record = lexicons[i][term]
				bin_files[i].seek (lex_record["position"]*4)
				bytes_readed = bin_files[i].read (lex_record["df"]*4)
				doc_ids.extend(struct.unpack ("%dI" % lex_record["df"], bytes_readed))
		return doc_ids
			
	def open_bin_files (self, index_files):
		bin_files = []
		for filename in index_files:
			bin_files.append(open (filename, "r"))
		return bin_files

	def close_bin_files (self, bin_files):
		for bin_file in bin_files:
			bin_file.close()
