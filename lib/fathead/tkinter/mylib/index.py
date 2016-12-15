import os.path
import re

from base64 import b64encode
from imp import find_module
from os import SEEK_END, SEEK_SET
from os.path import getmtime
from pydoc import locate as pydoc_locate
from struct import Struct

class Error(Exception): pass
class IndexCreateError(Error): pass
class IndexLoadError(Error): pass

def get_module_path(name):
	if "." not in name:
		try:
			f, p, _ = find_module(name)
			return p
		except ImportError:
			return None
	else:
		x = pydoc_locate(name)
		if not x:
			return None
		return x.__file__

def get_cached_path(path, cache_dir=".", must_exist=False):
	cache_dir = cache_dir or "."
	cached_path = os.path.join(cache_dir, b64encode(path, "+_"))
	cached_path = os.path.abspath(cached_path)
	if must_exist and not os.path.isfile(cached_path):
		raise CachePathError("cache file for '%s' not"
			" found in '%s'" % (path, cache_dir))
	return cached_path

class IndexFile(object):

	abi = Struct("ii")

	def __init__(self, path, mode="read"):
		assert mode in ("read", "write")
		self.path = path
		self.mode = mode
		self.file = None

	def __enter__(self):
		_mode = "wb" if self.mode == "write" else "rb"
		self.file = open(self.path, _mode)
		return self

	def __exit__(self, x, m, t):
		self.file.close()
		self.file = None

	def write(self, *args):
		self.file.write(self.abi.pack(*args))

	def read(self):
		return self.abi.unpack(self.file.read(self.abi.size))

	def get_count(self):
		mark = self.file.tell()
		self.file.seek(0, SEEK_END)
		size = self.file.tell()
		self.file.seek(mark, SEEK_SET)
		return size / self.abi.size

def create_line_index_for_module(name, cache_dir="."):
	p = get_module_path(name)
	if not p:
		raise IndexCreateError, "module '%s' not found" % name
	c = get_cached_path(p, cache_dir=cache_dir, must_exist=False)
	
	with IndexFile(c, "write") as i:
		with open(p, "rb") as f:
			for x in re.finditer(r"(?im)^(.*)$", f.read()):
				i.write(x.start(0), x.end(0))

class Index(object):

	def __init__(self):
		self.src_path = None
		self.cached_path = None
		self.file = None

	@classmethod
	def from_module(cls, name, cache_dir="."):
		index = Index()
		index.src_path = get_module_path(name)
		if not index.src_path:
			raise IndexLoadError, "file not found for module '%s'" % name
		index.cached_path = get_cached_path(index.src_path, cache_dir)
		return index

	def is_cached(self, pedantic=True):
		if not os.path.isfile(self.cached_path):
			return False
		if 0 == os.path.getsize(self.cached_path):
			return False
		# TODO: Change the cache file format to include
		#	some magic value in the header which would
		#	only be written after the file was created
		#	successfully (i.e. the tot number of lines).
		#	We can check this value for nonzero to tell
		#	if this is a valid cache file or not.
		if not pedantic:
			return True
		assert os.path.isfile(self.src_path)
		if (os.path.getmtime(self.src_path) >
				os.path.getmtime(self.cached_path)):
			return False
		return True

	def get_line_offsets(self, index):pass
	def _get_line_offsets(self, index, text_file, cache_file):pass
		


