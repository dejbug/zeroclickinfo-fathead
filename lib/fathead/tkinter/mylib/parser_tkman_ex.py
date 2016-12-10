# -*- coding: utf-8 -*-
"Classes for Tk-Docs parsing: Extractors."
import pprint
import re

from common import Pattern
from common import TkDocFile


class Extractor(object):
	def __init__(self, tdf):
		assert isinstance(tdf, TkDocFile)
		self.tdf = tdf

	def get_section_names(self):
		"""Return a list of available section header labels."""
		pattern = Pattern(r"(?i)\.SH +((?:\"[^\"]+?\")|(?:[^ ]+?))\n")
		return pattern.finditer(self.tdf.text)

	def get_section_line(self, label="NAME"):
		"""Return the first line below the section header with
		the given {label}."""
		pattern = Pattern(r"(?i)\.SH +%s\n+(.+?)\n" % label)
		return pattern.search(self.tdf.text)

	def get_block_lines(self, pattern):
		"""Return the consecutive lines of text below the
		line matching the {pattern}."""
		pattern = Pattern(pattern)
		x = pattern.search(self.tdf.text)
		# -- TODO: either modify pattern to match the block or use
		#	text-offset logic [i.e. {rest = self.tdf.text[x.end(0):]}].
		# -- NOTE: Perhaps it would be best to go through the
		#	man-page one line at a time? That is, a real parser
		#	instead of an extractor.

	def get_standard_options(self):
		"""Return the standard options block as a list of options."""
		pattern1 = Pattern(r"(?ims)^\.SO *$(.+?)^\.SE")
		pattern2 = Pattern(r"\-(.+?)(?:\t|\n)")
		text = pattern1.search(self.tdf.text)
		options = pattern2.finditer(text)
		return options

	def get_options(self):
		pattern = Pattern(r"(?im)\.OP +\\-(.+?)[ \n]")
		return pattern.finditer(self.tdf.text)


class TkDocParser(object):
	def __init__(self, tdf):
		assert isinstance(tdf, TkDocFile)
		self.tdf = tdf
		self.ex = Extractor(self.tdf)

	def __str__(self):
		return pprint.pformat(self.__dict__)

	def parse(self):
		s = self.ex.get_section_line("NAME")
		self.name, self.blurb = re.split(r' +\\- +', s)

		self.syn = self.ex.get_section_line("SYNOPSIS")
		# self.syn_html = get_html_from_groff(self.syn)

		self.std_opts = self.ex.get_standard_options()
		self.opts = self.ex.get_options()

