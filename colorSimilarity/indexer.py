# USAGE
# python index.py --dataset dataset --index index.csv

# import the necessary packages
from colorSimilarity.featureDescriptors.colorDescriptor import ColorDescriptor
import argparse
import glob
import cv2


class Indexer:
	def __init__(self):
		self.cd = ColorDescriptor((8, 12, 3))

	def extract_color_descriptor_features(self, image):
		"""Extracts Color Descriptor Based Features and encodes it as a string."""
		features = [str(feature) for feature in self.cd.describe(image)]
		string_encoded_features = ",".join(features)
		return string_encoded_features

	def detect_facial_presence(self, image):
		return []

	def index_image(self, image):
		features = [self.extract_color_descriptor_features(image), self.detect_facial_presence(image)]
		return features