import re

from abstract import disabled


@disabled("unused")
def extract(pattern, text, method="match"):
	# assert method in ("match", "search", "finditer")
	regex = re.compile(pattern)

	if method in ("match", "search"):
		x = getattr(regex, method)(text)
		if not x: return None
		return x.groups()
	elif method in ("finditer", "iter"):
		xx = regex.finditer(text)
		return [x.groups() for x in xx]
	raise ValueError


@disabled("fixme")
def get_html_from_groff(text):
	# -- FIXME: This is too naive. It seems groff markup is flat, i.e.
	#	it does not support nesting: an opening tag r'\f[B|I]' will
	#	act like a closing tag r'\fR' on all unclosed prior tags.
	#	Also there may be all sorts of characters inside a marked-up
	#	text: especially whitespaces and escaped hyphens r'\-'. In
	#	other words, more than only TCL identifiers may be marked up.
	def callback(x):
		return r'<{0}>{1}</{0}>'.format(x.group(1).lower(), x.group(2))
	return re.sub(r'(?:\\f(B|I))(.+?)(?:\\fR)', callback, text)


Patterns = collections.OrderedDict((
	('sh', r"(?im)^\.SH +(.+)$"),
	('op', r"(?im)^\.OP +(.+)$"),
	('so_block', r"(?ims)^\.SO *$(.+?)^\.SE"),
	('so_items', r"\\(-.+?)\\[tn]"),
))

