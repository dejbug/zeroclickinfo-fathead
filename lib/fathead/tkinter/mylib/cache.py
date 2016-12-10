import pickle
import os.path

CACHE_DIR = "download/cache"

def to_path(slot):
	return os.path.join(CACHE_DIR, "cache.%05d.pickle" % slot)

def save(slot, obj):
	assert isinstance(slot, (int, long))
	with open(to_path(slot), "wb") as f:
		pickle.dump(obj, f, -1)

def load(slot):
	assert isinstance(slot, (int, long))
	with open(to_path(slot), "rb") as f:
		return pickle.load(f)
