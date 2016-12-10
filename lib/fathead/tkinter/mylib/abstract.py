

class disabled(object):
	"""A decorator to flag functions as unusable."""

	def __init__(self, reason="unused"):
		self.reason = reason or ""
		
	def __call__(self, obj):
		return self._dummy

	def _dummy(self, *aa, **kk):
		raise NotImplementedError(self.reason)

