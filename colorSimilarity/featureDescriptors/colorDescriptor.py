# import the necessary packages
import numpy as np
import cv2


class ColorDescriptor:
	"""
	Class splits the image into 5 zones, and finds the HSV color histogram for each zone.
	These 5 sets of histograms are returned as features.
	Courtesy Adrian Rosebrock and PyImageSearch.
	"""
	def __init__(self, bins):
		# store the number of bins for the 3D histogram
		self.bins = bins
		self.dtype = "uint8"

	@staticmethod
	def get_image_central_measures(image):
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))
		return h, w, cX, cY

	def get_zonal_segments(self, image):
		h, w, cX, cY = self.get_image_central_measures(image)
		# divide the image into four rectangles/segments (top-left,
		# top-right, bottom-right, bottom-left)
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
					(0, cX, cY, h)]
		return segments

	def central_mask(self, image):
		# construct an elliptical mask representing the center of the image
		h, w, cX, cY = self.get_image_central_measures(image)
		(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
		ellip_mask = np.zeros(image.shape[:2], dtype = self.dtype)
		cv2.ellipse(ellip_mask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
		return ellip_mask

	def get_image_masks(self, image):
		# grab the dimensions and compute the center of the image
		central_elliptical_mask = self.central_mask(image)
		masks = [central_elliptical_mask]
		# construct a mask for each corner of the image, subtracting
		# the elliptical center from it
		for (startX, endX, startY, endY) in self.get_zonal_segments(image):
			corner_mask = np.zeros(image.shape[:2], dtype = self.dtype)
			cv2.rectangle(corner_mask, (startX, startY), (endX, endY), 255, -1)
			masks.append(cv2.subtract(corner_mask, central_elliptical_mask))
		return masks

	def histogram(self, image, mask):
		# extract a 3D color histogram from the masked region of the
		# image, using the supplied number of bins per channel
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])
		return cv2.normalize(hist, hist).flatten()

	def describe(self, input_image):
		# convert the image to the HSV color space and initialize
		# the features used to quantify the image
		image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
		features = []
		masks = self.get_image_masks(image)

		for mask in masks:
			# extract a color histogram from the image, then update the feature vector
			hist = self.histogram(image, mask)
			features.extend(hist)
		return features

