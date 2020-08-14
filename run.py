from ImageRepresentation.Image import Image
from featureExtraction.indexer import Indexer
from HelperFunctions.mysqlConnector import get_conn
import os


image_names = ["102900.png", "102901.png", "103000.png", "103001.png", "103002.png", "103101.png", "103102.png"]

mysql_connector = get_conn(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PWD"))
for image_name in image_names:
	image_path = "dataset/{}".format(image_name)
	print(image_path)
	img = Image(image_path, mysql_connector)
	indexer = Indexer(mysql_connector)
	indexer.index_image(img)

