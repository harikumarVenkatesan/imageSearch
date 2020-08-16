def insert_color_descriptor(image_id, features):
	query = """
			insert into image_search.color_descriptor_features (image_id, features) VALUES ('{}', '{}')
	""".format(image_id, features)
	return query


def create_image_color_descriptor_table():
	query = """
				create table image_search.color_descriptor_features(
				   image_id INT NOT NULL,
				   features TEXT NOT NULL,
				   PRIMARY KEY ( image_id )
				);
		"""
	return query