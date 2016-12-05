import re
import os
import codecs
from pprint import pprint


def to_str(obj):
	if isinstance(obj, str):
		return obj
	elif isinstance(obj, unicode):
		return obj.encode("utf8")
	else:
		try:
			return obj.read()
		except AttributeError: pass
	raise ValueError


def iter_pattern(f, p):
	for x in re.finditer(p, to_str(f)):
		yield x.groups()


def list_sections(f):
	for g in iter_pattern(f, r"(?im)^\.SH +(.+)$"):
		print g


def list_options(f):
	for g in iter_pattern(f, r"(?im)^\.OP +(.+)$"):
		print g


def get_so_block(f):
	i = iter_pattern(f, r"(?ims)^\.SO *$(.+?)^\.SE")
	return list(i)[0:1]


def iter_so_items(f):
	b = unicode(get_so_block(f))
	for g in iter_pattern(b, r"\\(-.+?)\\[tn]"):
		yield g[0]


def iter_files(path="doc", ext=".n", recurse=False):
	for r,dd,nn in os.walk(path):
		for n in nn:
			if n.endswith(ext):
				yield os.path.join(r,n)
		if not recurse: break
		

def openf(path):
	return codecs.open(path, "rb", "utf8")


def test1():
	with codecs.open("doc/button.n", "rb", "utf8") as f:
		so = list(iter_so_items(f))
		pprint(sorted(so))


def test2():
	for p in iter_files(ext=".n"):
		print p
		list_sections(openf(p))
		print "--"


def extract(f, pattern, default=None):
	x = re.search(pattern, to_str(f))
	if not x: return default
	g = x.groups()
	return g[0] if len(g) == 1 else g


class doc_n(object):
	def __init__(self, path):
		assert isinstance(path, (str, unicode))
		with codecs.open(path, "rb", "utf8") as f:
			
			t = extract(f, "(?ms)^.SH +NAME.*?$(.+?)$").strip()
			self.title, self.desc = extract(t, r"(.+?) *\\- *(.+)")


def iter_n():
	return iter_files(ext=".n")



if "__main__" == __name__:

	tt = []

	for p in iter_files(ext=".n"):
		tt.append(doc_n(p))
	
	for p in sorted(tt, key=lambda x: x.title):
		pprint(p.__dict__)

