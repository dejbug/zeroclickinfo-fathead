#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_1():
	"""A rough-and-dirty pydoc-to-html converter for Tkinter.py ."""
	from mylib import cache
	from mylib.parser_pydoc import save_pydocs, write_pydoc_html
	
	# -- Use a cached version of the pydocs.
	try:
		cc = cache.load(1)
	except IOError:
		# -- No cached version found; so make one.
		save_pydocs()
		cc = cache.load(1)

	with open("downloads/test.html", "wb") as f:
		write_pydoc_html(f, cc)

def test_2():
	from mylib.common import Downloads
	
	# -- Print the number of man files to parse (i.e.
	#	those that end in "*.n"). The "*.3" belong to
	#	Tk's C API and are of no interest for now.
	print len(list(Downloads.iter_tk_doc_files()))

def test_3():
	"""I like this approach best. Since we really need to
	scan through the entire file anyway. And it's nicely
	structured in a line-wise fashion, let's make use of
	that."""
	import pprint
	from mylib.common import Downloads
	from mylib.parser_tkman_sc import LineParser

	for d in Downloads.iter_tk_doc_files():

		for typ, line in LineParser(d):
			if typ == "tag": print line
			elif typ == "txt": pprint.pprint(line)

		break

def test_4():
	"""The old approach. Wasn't too slow, but meh."""
	from mylib.common import Downloads
	from mylib.parser_tkman_ex import Extractor
	from mylib.parser_tkman_ex import TkDocParser

	for d in Downloads.iter_tk_doc_files():

		print d.name
		
		ex = Extractor(d)
		print ex.get_section_names()
		print ex.get_section_line("NAME")
		
		par = TkDocParser(d)
		par.parse()
		print par

		break

def test_5():
	"""A better Tkinter.py scanner: now reads arguments ."""
	from imp import find_module
	from mylib import cache
	from mylib.index import Index
	from mylib.parser_pydoc import save_pydocs
	from mylib.parser_pydoc import is_class
	
	# -- Use a cached version of the pydocs.
	try:
		cc = cache.load(1)
	except IOError:
		# -- No cached version found; so make one.
		save_pydocs()
		cc = cache.load(1)

	# from mylib import index
	# index.create_line_index_for_module("Tkinter", cache_dir="download")

	ii = Index.from_module("Tkinter", cache_dir="download")
	print ii.__dict__
	print ii.is_cached()
	return

	for c in cc.values():
		if is_class(c):
			print c.name, c.lineno


def main():
	# test_1()
	# test_2()
	# test_3()
	# test_4()
	test_5()


if "__main__" == __name__:
	main()
