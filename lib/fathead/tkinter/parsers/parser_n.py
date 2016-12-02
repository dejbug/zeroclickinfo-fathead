import re
import codecs
from pprint import pprint


def iter_pattern(x, p):
	try:
		return iter_pattern_f(x, p)
	except AttributeError: pass
	try:
		return iter_pattern_s(x, p)
	except AttributeError: pass
	raise ValueError


def iter_pattern_f(f, p):
	for x in re.finditer(p, f.read()):
		yield x.groups()


def iter_pattern_s(s, p):
	for x in re.finditer(p, s):
		yield x.groups()


def list_sections(f):
	for g in iter_pattern_f(f, r"(?im)^\.SH +(.+)$"):
		print g


def list_options(f):
	for g in iter_pattern_f(f, r"(?im)^\.OP +(.+)$"):
		print g


def get_so_block(f):
	i = iter_pattern_f(f, r"(?ims)^\.SO *$(.+?)^\.SE")
	return list(i)[0:1]


def iter_so_items(f):
	b = get_so_block(f)
	print unicode(b)
	for g in iter_pattern_s(unicode(b), r"\\(-.+?)\\[tn]"):
		yield g


if "__main__" == __name__:
	with codecs.open("doc/button.n", "rb", "utf8") as f:
		so = list(iter_so_items(f))
		pprint(sorted(so))

		



