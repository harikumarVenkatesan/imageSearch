from FeatureExtraction.ColorSimilarity.colorDescriptor import ColorDescriptor
from ImageRepresentation.Image import Image
from FeatureExtraction.SqlQueries import insert_color_descriptor
from HelperFunctions.MysqlConnector import run_query_noop
from HelperFunctions.HelperFunctions import serialize_features


class Indexer:
	def __init__(self, mysql_connector):
		self.cd = ColorDescriptor((8, 12, 3))
		self.mysql_connector = mysql_connector

	def extract_color_descriptor_features(self, image_object):
		"""Extracts Color Descriptor Based Features and encodes it as a string."""
		if not image_object.has_color_descriptor:
			features = [str(feature) for feature in self.cd.describe(image_object.image)]
			serialized_features = serialize_features(features)
			print(len(serialized_features))
			run_query_noop(self.mysql_connector, insert_color_descriptor(image_object.image_id, serialized_features))
		else:
			print("Already has image descriptor. Skipping")
		return True

	def detect_facial_presence(self, image):
		return []

	def index_image(self, image_object: Image):
		self.extract_color_descriptor_features(image_object)
