import os
import io

class CollectionPrinter:
	def __init__ (printer, collection):
		printer.collection = collection

	def print_terms (printer, output_filename):
		file = io.open (output_filename, mode="w", encoding="UTF-8")
		terms = printer.collection.get_terms_sorted_by_freq ()
		for term in terms:
			file.write ("%s  CF:%i  DF:%i%s" % (term.name, term.cf, term.df, os.linesep))
		file.close ()
		
	def print_statistics (printer, output_filename):
		collection = printer.collection
		shortest = collection.get_shortest_document ()
		longest = collection.get_longest_document ()
		file = open (output_filename, "w")
		file.write ("Documentos procesados: %i%s" % (collection.get_document_count(), os.linesep))
		file.write ("Tokens extraidos: %i%s" %(collection.get_token_count(), os.linesep))
		file.write ("Terminos extraidos: %i%s" %(collection.get_term_count(), os.linesep))
		file.write ("Promedio de tokens en documento: %d%s" %(collection.get_avg_tokens_per_document(), os.linesep))
		file.write ("Promedio de terminos en documento: %d%s" %(collection.get_avg_terms_per_document(), os.linesep))
		file.write ("Largo promedio de termino: %d.2 caracteres%s" %(collection.get_avg_term_length(), os.linesep))
		file.write ("Documento mas corto:%s" %(os.linesep))
		file.write ("\tTokens extraidos: %i%s" %(shortest.get_token_count(), os.linesep))
		file.write ("\tTerminos extraidos: %i%s" %(shortest.get_term_count(), os.linesep))
		file.write ("Documento mas largo:%s" %(os.linesep))
		file.write ("\tTokens extraidos: %i%s" %(longest.get_token_count(), os.linesep))
		file.write ("\tTerminos extraidos: %i%s" %(longest.get_term_count(), os.linesep))
		file.write ("Terminos hapax: %i%s" % (len (collection.get_hapax()), os.linesep))
		file.close ()
		
	def print_top_ten (printer, output_filename):
		most_frequent_terms = printer.collection.get_top_freq_terms (10)
		less_frequent_terms = printer.collection.get_bottom_freq_terms (10)
		file = open (output_filename, "w")
		file.write ("Terminos mas frecuentes:%s" % (os.linesep))
		for term in most_frequent_terms:
			file.write ("\t%s  CF=%i%s" % (term.name, term.cf, os.linesep))
		file.write ("Terminos menos frecuentes:%s" % (os.linesep))
		for term in less_frequent_terms:
			file.write ("\t%s  CF=%i%s" % (term.name, term.cf, os.linesep))
		file.close ()
		
