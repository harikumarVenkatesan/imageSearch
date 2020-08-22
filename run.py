from ImageRepresentation.Image import Image
from Indexer.Indexer import Indexer
from HelperFunctions.MysqlConnector import get_conn
import os
import cv2
from Searcher.Searcher import Searcher
from FeatureExtraction.FacialRecognition.ExtractEmbeddings import ExtractEmbeddings
from FeatureExtraction.FacialRecognition.TrainFacialRecognitionModel import TrainFacialRecognitionModel
from imutils import paths
import numpy as np
#
# image_names = ["102900.png", "102901.png", "103000.png", "103001.png", "103002.png", "103101.png", "103102.png"]
#
# make static to avoid thread locks.
print(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PWD"))
mysql_connector = get_conn(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PWD"))
# for image_name in image_names:
# 	image_path = "dataset/{}".format(image_name)
# 	print(image_path)
# 	img = Image(path = image_path, mysql_connector = mysql_connector)
# 	indexer = Indexer(mysql_connector)
# 	indexer.index_image(img)
#
# query_image_path = "dataset/102900.png"
# query_image = Image(path = query_image_path, mysql_connector = mysql_connector)
# searcher = Searcher(mysql_connector)
# op = searcher.search(query_image.image_id, 3)

# Running facial feature extraction for a single image.
face_detection_model_directory = "/Users/harikumarvenkatesan/Documents/GitHub/imageSearch/FeatureExtraction/FacialRecognition/face_detection_model/"
embedding_model_directory = "/Users/harikumarvenkatesan/Documents/GitHub/imageSearch/FeatureExtraction/FacialRecognition/"
#
extract_facial_features = ExtractEmbeddings("", face_detection_model_directory, embedding_model_directory, 0.5, mysql_connector)
image_paths = paths.list_images("/Users/harikumarvenkatesan/Documents/GitHub/imageSearch/dataset/facial_detection/training/")
for image_path in image_paths:
	tag = image_path.split(os.path.sep)[-2]
	print(image_path, tag)
	image = cv2.imread(image_path)
	extract_facial_features.process_facial_feature_extraction(image, tag, True)
	print(extract_facial_features.counter)

persist_disk = {"model_path": "op/models/recognizer.pickle", "label_encoder_path": "op/models/label_encoder.pickle"}
self = TrainFacialRecognitionModel(mysql_connector)
self.train_ml_model("SVM", persist_disk)

test_image_paths = paths.list_images("/Users/harikumarvenkatesan/Documents/GitHub/imageSearch/dataset/facial_detection/test/")
for test_image_path in test_image_paths:
	test_image = cv2.imread(test_image_path)
	tag = test_image_path.split(os.path.sep)[-1]
	facial_features = extract_facial_features.process_facial_feature_extraction(test_image, "", False)
	preds = self.recognizer.predict_proba([facial_features])[0]
	j = np.argmax(preds)
	proba = preds[j]
	name = self.label_encoder.classes_[j]
	print(name, tag, proba, list(zip(preds, self.label_encoder.classes_)))
