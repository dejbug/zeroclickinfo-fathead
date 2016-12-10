# -*- coding: utf-8 -*-
"Classes for Tk-Docs parsing: Scanner."
import re

from common import TkDocFile


class LineParser(object):
	def __init__(self, tdf):
		assert isinstance(tdf, TkDocFile)
		self.tdf = tdf

	def __iter__(self):
		block = []

		for x in re.finditer(r"(?im)^(.+)$", self.tdf.text):
			line = x.group(1)
			if line.startswith("'\\\""):
				yield "cmt", line
			elif line.startswith("."):
				if block:
					yield "txt", block
					block = []
				yield "tag", line
			else:
				# block.append(get_html_from_groff(line))
				block.append(line)	

		if block:
			yield "txt", block

