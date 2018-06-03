#!/usr/bin/env python

file_input = open ("CISI.ALL", "r")
file_output = open ("CISI.TREC", "w")
next_is_title = False

for line in file_input:
	if (line.startswith (".I ")):
		skip_next = False
		num = line.replace (".I ", "").replace("\r\n", "")
		file_output.write ("<DOC>\r\n<DOCNO>%s</DOCNO>\r\n" % num)
	elif (line.startswith (".T")):
		pass
	elif (line.startswith (".A")):
		pass
	elif (line.startswith (".W")):
		pass
	elif (line.startswith (".X")):
		file_output.write("</DOC>\n")
		skip_next = True
	elif skip_next:
		pass
	else:
		file_output.write (line)

file_input.close()
file_output.close()

