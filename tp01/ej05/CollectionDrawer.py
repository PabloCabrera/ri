# -*- coding: utf-8 -*-

import matplotlib.pyplot as plotter

class CollectionDrawer:
	def __init__ (drawer, collection):
		drawer.collection = collection

	def draw (drawer):
		terms = drawer.collection.get_terms_sorted_by_freq ()
		term_count = len (terms)
		points = list ()
		index = 0
		fig = plotter.figure ()
		coords_x = list ()
		coords_y = list ()
		while index < term_count:
			coords_x.append (index)
			coords_y.append (terms[index].cf)
			if index % 100 == 0:
				print index
			index += 1
		plotter.plot (coords_x, coords_y, "o")
		plotter.savefig ("lineal.png")
		plotter.loglog ()
		plotter.savefig ("loglog.png")


