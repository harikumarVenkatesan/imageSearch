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


def insert_facial_features(name, facial_features):
	query = """
			insert into image_search.facial_features_tagged (name, features) VALUES ('{}', '{}')
	""".format(name, facial_features)
	return query


def create_facial_features_tagged_table():
	query = """
				create table image_search.facial_features_tagged(
				   name TEXT NOT NULL,
				   features TEXT NOT NULL
				);
		"""
	return query


def get_labeled_facial_data():
	query = """
			select * from image_search.facial_features_tagged;
	"""
	return query