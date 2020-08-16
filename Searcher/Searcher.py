# import the necessary packages
import numpy as np
from HelperFunctions.mysqlConnector import run_query_noop, run_query_op
from Searcher.searcher_sql_queries import get_features
from distanceMeasures.DistanceMeasures import DistanceMeasures
from ImageRepresentation.similarImage import SimilarImage


class Searcher:
	def __init__(self, mysql_connector):
		self.mysql_connector = mysql_connector
		return

	@staticmethod
	def deserialize_features(feature_list, dtype = "float32"):
		return np.asarray(feature_list.split(","), dtype = dtype)

	def search(self, query_image_id, limit = 10):
		indexed_features_data = run_query_op(self.mysql_connector, get_features("image_search.color_descriptor_features"))
		indexed_features_data['float_features'] = indexed_features_data["features"].apply(self.deserialize_features)
		query_features_data = run_query_op(self.mysql_connector, get_features("image_search.color_descriptor_features",
																			  image_id = query_image_id))
		query_features = self.deserialize_features(query_features_data['features'].iloc[0])

		indexed_features_data['similarity_score'] = indexed_features_data["float_features"].apply(
			lambda x: DistanceMeasures.chi2_distance(x, query_features))
		top_results = indexed_features_data.nsmallest(limit, ["similarity_score"])
		return [SimilarImage(image_id = row['image_id'], mysql_connector = self.mysql_connector,
							 similarity_score = row['similarity_score']) for _, row in top_results.iterrows()]
