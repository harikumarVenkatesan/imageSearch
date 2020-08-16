from ImageRepresentation.Image import Image


class SimilarImage(Image):
	def __init__(self, image_id, mysql_connector, similarity_score):
		Image.__init__(self, image_id = image_id, mysql_connector = mysql_connector)
		self.similarity_score = similarity_score
