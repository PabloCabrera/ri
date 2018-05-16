# -*- coding: utf-8 -*-

import matplotlib.pyplot as plotter
import os
import copy
import numpy
import math

class CollectionDrawer:
	def __init__ (drawer, collection):
		drawer.collection = collection

	def draw (drawer, exclude):
		terms = None
		if (exclude > 0):
			terms = drawer.exclude_terms (exclude);
		else:
			terms = drawer.collection.get_terms_sorted_by_freq ()

		term_count = len (terms)
		points = list ()
		index = 0
		coords_x = list ()
		coords_y = list ()
		while index < term_count:
			coords_x.append (index)
			coords_y.append (terms[index].cf)
			index += 1

		try:
			os.mkdir ("img")
		except OSError:
			pass

		drawer.plot_linear (coords_x, coords_y, "img/lineal_%d.png" % exclude)
		drawer.plot_loglog (coords_x, coords_y, "img/loglog_%d.png" % exclude)

	def plot_linear (drawer, coords_x, coords_y, filename):
		fig = plotter.figure ()
		plotter.plot (coords_x, coords_y, "o")
		plotter.savefig (filename)
		plotter.close(fig)

	def plot_loglog (drawer, coords_x, coords_y, filename):
		fig = plotter.figure ()
		log_x = []
		log_y = []
		for x in coords_x:
			log_x.append (math.log (x+1))
		for y in coords_y:
			log_y.append (math.log (y))
		recta = numpy.polyfit (log_x, log_y, 1)
		y_ajuste = []
		for x in log_x:
			y_ajuste.append (recta[0]*x + recta[1])
		error_sum = 0
		for pos in (xrange (0, len (log_x))):
			error_sum += pow (log_y[pos] - y_ajuste[pos], 2)
		mse = math.sqrt (error_sum) / len (log_x)
		plotter.title ("Error medio cuadrado: %.5f" % mse)
		plotter.plot (log_x, log_y, "bo")
		plotter.plot (log_x, y_ajuste, "r")
		plotter.savefig (filename)
		plotter.close(fig)

	def exclude_terms (drawer, exclude):
		total = drawer.collection.get_token_count ()
		cut = total*exclude/2
		terms = drawer.collection.get_terms_sorted_by_freq ()
		cutted = 0
		total_cutted = 0
		if (exclude > 0):

			# Cut tail
			while (cutted < (cut/100)):
				term_cutted = terms.pop ()
				cutted += term_cutted.cf

			total_cutted += cutted

			# Cut head
			cutted = 0
			terms.reverse ()
			while (cutted < (cut/100)):
				term_cutted = terms.pop ()
				cutted += term_cutted.cf
			total_cutted += cutted
			terms.reverse ()

		return terms
		
