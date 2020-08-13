def insert_image_path_query(image_path):
	query = """
		insert into image_search.image (image_path) VALUES ('{}')  
	""".format(image_path)
	return query


def get_image_id_query(image_path):
	query = """
			select image_id from image_search.image 
			where image_path = '{}'
	""".format(image_path)
	return query


def create_image_table():
	query = """
			create table image_search.image(
			   image_id INT NOT NULL AUTO_INCREMENT,
			   image_path VARCHAR(100) NOT NULL,
			   PRIMARY KEY ( image_id ),
			   UNIQUE (image_path)
			);
	"""
	return query