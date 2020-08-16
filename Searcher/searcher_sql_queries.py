def get_features(table_name, image_id = None):
	query = """
				select * from {}
				{} 
		""".format(table_name, "{}")
	if image_id:
		filter_clause = "where image_id = {}".format(image_id)
	else:
		filter_clause = ""
	query = query.format(filter_clause)
	return query
