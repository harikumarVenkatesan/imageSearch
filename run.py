from ImageRepresentation.Image import Image
from FeatureExtraction.Indexer import Indexer
from HelperFunctions.MysqlConnector import get_conn
import os
from Searcher.Searcher import Searcher

image_names = ["102900.png", "102901.png", "103000.png", "103001.png", "103002.png", "103101.png", "103102.png"]

# make static to avoid thread locks.
mysql_connector = get_conn(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PWD"))
for image_name in image_names:
	image_path = "dataset/{}".format(image_name)
	print(image_path)
	img = Image(path = image_path, mysql_connector = mysql_connector)
	indexer = Indexer(mysql_connector)
	indexer.index_image(img)

query_image_path = "dataset/102900.png"
query_image = Image(path = query_image_path, mysql_connector = mysql_connector)
searcher = Searcher(mysql_connector)
op = searcher.search(query_image.image_id, 3)


