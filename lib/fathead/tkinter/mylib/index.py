import os.path
import re

from base64 import b64encode
from imp import find_module
from os import SEEK_END, SEEK_SET
from os.path import getmtime
from pydoc import locate as pydoc_locate
from struct import Struct


class Error(Exception): pass
class ModulePathFindError(Error): pass
class IndexCreateError(Error): pass
class IndexLoadError(Error): pass
class IndexLoadError(Error): pass


def file_like(obj):

	def obj_open(o, mode="rb"):
		if o.file: o.file.close()
		o.file = open(o.path, mode)
		return o

	def obj_close(o):
		if o.file: o.file.close()
		o.file = None
		return o

	def obj_enter(o):
		return o.open()

	def obj_exit(o, x, m, t):
		o.close()

	if not hasattr(obj,  "open"):
		setattr(obj, "open", obj_open)
	if not hasattr(obj, "close"):
		setattr(obj, "close", obj_close)
	if not hasattr(obj, "__enter__"):
		setattr(obj, "__enter__", obj_enter)
	if not hasattr(obj, "__exit__"):
		setattr(obj, "__exit__", obj_exit)

	return obj


def find_module_path(dotted_name):
	if "." not in dotted_name:
		try:
			f, p, _ = find_module(dotted_name)
			return p
		except ImportError:
			raise ModulePathFindError("file not found for module '%s'" %
				dotted_name)
	else:
		x = pydoc_locate(dotted_name)
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


@file_like
class IndexFile(object):

	abi = Struct("ii")

	def __init__(self, path, mode="read"):
		assert mode in ("read", "write")
		self.path = path
		self.mode = mode
		self.file = None

	def open(self):
		_mode = "wb" if self.mode == "write" else "rb"
		self.file = open(self.path, _mode)
		return self

	def close(self):
		self.file.close()
		self.file = None

	def write(self, *args):
		self.file.write(self.abi.pack(*args))

	def read(self):
		return self.abi.unpack(self.file.read(self.abi.size))

	def seek(self, item=0):
		self.file.seek(self.abi.size * item, SEEK_SET)

	def get_count(self):
		mark = self.file.tell()
		self.file.seek(0, SEEK_END)
		size = self.file.tell()
		self.file.seek(mark, SEEK_SET)
		return size / self.abi.size


def create_line_index_for_module(name, cache_dir="."):

	p = find_module_path(name)
	if not p:
		raise IndexCreateError, "module '%s' not found" % name
	c = get_cached_path(p, cache_dir=cache_dir, must_exist=False)
	
	with IndexFile(c, "write") as i:
		with open(p, "rb") as f:
			for x in re.finditer(r"(?im)^(.*)$", f.read()):
				i.write(x.start(0), x.end(0))


class ModulePath(object):

	def __init__(self, dotted_name, cache_dir="."):
		self.cache_dir = cache_dir or "."
		self.name = dotted_name
		self.path = find_module_path(self.name)
		self.temp = get_cached_path(self.path, self.cache_dir)


@file_like
class ModuleFile(object):

	def __init__(self, module_path):
		assert isinstance(module_path, ModulePath)
		self.module_path = module_path
		self.file = None

	@property
	def path(self):
		return self.module_path.path

	def extract_range(self, begin, end):
		self.file.seek(begin)
		return self.file.read(end - begin)


class Index(object):

	def __init__(self):
		self.module_path = None
		self.module_file = None
		self.index_file = None

	@classmethod
	def from_module(cls, dotted_name, cache_dir="."):
		index = Index()
		index.module_path = ModulePath(dotted_name, cache_dir)
		index.module_file = ModuleFile(index.module_path)
		index.index_file = IndexFile(index.module_path.temp, "read")
		return index

	def is_cached(self, pedantic=True):
		if not os.path.isfile(self.module_path.temp):
			return False
		if 0 == os.path.getsize(self.module_path.temp):
			return False
		# TODO: Change the cache file format to include
		#	some magic value in the header which would
		#	only be written after the file was created
		#	successfully (i.e. the tot number of lines).
		#	We can check this value for nonzero to tell
		#	if this is a valid cache file or not.
		if not pedantic:
			return True
		assert os.path.isfile(self.module_path.path)
		if (os.path.getmtime(self.module_path.path) >
				os.path.getmtime(self.module_path.temp)):
			return False
		return True

	def __enter__(self):
		self.module_file.open()
		self.index_file.open()
		return self
				
	def __exit__(self, x, m, t):
		self.index_file.close()
		self.module_file.close()

	def get_line_offsets(self, line_index):
		self.index_file.seek(line_index)
		return self.index_file.read()

	def get_line_text(self, line_index):
		offsets = self.get_line_offsets(line_index)
		return self.module_file.extract_range(*offsets)
		
