import pprint
import pyclbr
import pydoc
import re

import cache


def save_pydocs():
	"""Run the python class browser on Tkinter and cache the result."""
	# -- Save the dict.
	cc = pyclbr.readmodule_ex("Tkinter")
	cache.save(1, cc)
	# -- Save the dict as a sorted list of tuples, with each object
	#	prepended by its name.
	cc = sorted([(c.name, c) for c in cc.values()], key=lambda x: x[0])
	cache.save(2, cc)


def is_class(x):
	return isinstance(x, pyclbr.Class)


def is_func(x):
	return isinstance(x, pyclbr.Function)


def get_imp_str(c_or_f, m=None):
	"""Return import string for a (pyclbr) Class or Function object."""
	s = "Tkinter.%s" % (c_or_f.name, )
	return "%s.%s" % (s, m) if m else s


def get_pydoc_by_imp_str(s):
	x = pydoc.locate(s)
	return pydoc.getdoc(x)


def print_class_info(c):
	print
	print " -------------------------------------------- "
	print
	print " ======================= Name "
	print c.name
	print " =============== Base Classes "
	pprint([x.name for x in c.super])
	print " ==================== Methods "
	pprint(c.methods)


def print_func_info(c):
	print
	print " -------------------------------------------- "
	print
	print " ======================= Name "
	print c.name


def write_pydoc_html(f, cc=None):
	"""Save a little HTML version of Tkinter's pydoc."""
	
	f.write('<!DOCTYPE html><html><head><title>test1.html</title>'
		'<link rel="stylesheet" href="default.css"></head><body>\n')

	cc = cc or cache.load(1)

	for x in cc.values():
		xs = get_imp_str(x)

		if is_class(x):
			cdoc = get_pydoc_by_imp_str(xs)
			cdoc = re.sub(r'[\r\n]+', '<br>', cdoc)

			f.write('<p class="cls">\n')
			f.write('<span class="title">%s</span>\n' % xs)
			f.write('<span class="doc">%s</span>\n' % cdoc)
			f.write('<div class="mtds">\n')
			
			for m in x.methods:
				ms = get_imp_str(x, m)
				mdoc = get_pydoc_by_imp_str(ms)
				# mdoc = re.sub(r'[\r\n]+', '<br>', mdoc)

				f.write('\t<div class="mtd">\n')
				f.write('\t\t<span class="title">%s</span>\n' % ms)
				f.write('\t\t<span class="doc"><pre>%s</pre></span>\n' % mdoc)
				f.write('\t</div>')
			f.write("</div></p>\n")

		elif is_func(x):
			fdoc = get_pydoc_by_imp_str(xs)
			f.write('<p class="fnc">\n')
			f.write('<span class="title">%s</span>\n' % xs)
			f.write('<span class="doc">%s</span>\n' % fdoc)
			f.write('</p>\n')

	f.write("</body></html>")

