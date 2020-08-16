import numpy as np


class DistanceMeasures:
	def __init__(self):
		return

	@staticmethod
	def chi2_distance(hist_a, hist_b, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist_a, hist_b)])
		return d
