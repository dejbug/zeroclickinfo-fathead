# -*- coding: utf-8 -*-
import os
import re


class Pattern(object):
	def __init__(self, pattern):
		self.regex = re.compile(pattern)

	@classmethod
	def to_groups(cls, x):
		if not x: return None
		if len(x.groups()) == 0: return x.group(0)
		if len(x.groups()) == 1: return x.group(1)
		return x.groups()

	def match(self, text):
		return self.to_groups(self.regex.match(text))

	def search(self, text):
		return self.to_groups(self.regex.search(text))

	def finditer(self, text):
		xx = self.regex.finditer(text)
		return [self.to_groups(x) for x in xx]


class TkDocFile(object):
	PATH_MATCHER = re.compile(r'^.+\.n$')

	def __init__(self, path):
		self.path = path
		self.name = os.path.split(self.path)[1]
		self._text = None

	@classmethod
	def is_valid_path(cls, path):
		return not not cls.PATH_MATCHER.match(path)

	@property
	def text(self):
		if None == self._text:
			self.load()
		return self._text

	def load(self):
		if None == self._text:
			with open(self.path, "rb") as f:
				self._text = f.read()
		return self._text


class Downloads(object):
	ROOT = "download"

	@classmethod
	def get_tk_doc_path(cls):
		return os.path.abspath(os.path.join(cls.ROOT, "tk8.6.1/doc"))

	@classmethod
	def iter_tk_doc_files(cls):
		doc_path = cls.get_tk_doc_path()
		for t,dd,nn in os.walk(doc_path):
			# for n in sorted(nn):
			for n in nn:
				if TkDocFile.is_valid_path(n):
					yield TkDocFile(os.path.join(doc_path, n))

