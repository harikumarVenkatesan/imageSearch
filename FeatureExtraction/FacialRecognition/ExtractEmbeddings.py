# USAGE
# python extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle \
#	--detector face_detection_model --embedding-model openface_nn4.small2.v1.t7

# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
import os
from HelperFunctions.HelperFunctions import serialize_features
from HelperFunctions.MysqlConnector import run_query_noop
from FeatureExtraction.SqlQueries import insert_facial_features


def replicate_args():
	args = {"dataset": "dataset", "embeddings": "output/embeddings.pickle",
			"detector": "face_detection_model", "embedding_model": "openface_nn4.small2.v1.t7",
			"confidence": 0.5}
	return args


class ExtractEmbeddings:
	def __init__(self, labeled_dataset_path, face_detection_model_directory, embedding_model_directory, confidence, mysql_connector):
		self.labeled_images = list(paths.list_images(labeled_dataset_path))
		self.proto_path = os.path.sep.join([face_detection_model_directory, "deploy.prototxt"])
		self.model_path = os.path.sep.join([face_detection_model_directory, "res10_300x300_ssd_iter_140000.caffemodel"])
		self.embedding_model_path = os.path.sep.join([embedding_model_directory, "openface_nn4.small2.v1.t7"])
		self.facial_detector = cv2.dnn.readNetFromCaffe(self.proto_path, self.model_path)
		self.embedder = cv2.dnn.readNetFromTorch(self.embedding_model_path)
		self.confidence = confidence
		self.mysql_connector = mysql_connector
		self.counter = 0
		return

	def increase_counter(self):
		self.counter = self.counter + 1

	def get_face_detections(self, image_blob):
		self.facial_detector.setInput(image_blob)
		detections = self.facial_detector.forward()
		return detections

	def identify_facial_bounding_box(self, detections, h, w):
		i = np.argmax(detections[0, 0, :, 2])
		confidence = detections[0, 0, i, 2]
		if confidence > self.confidence:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			return [(startY, endY), (startX, endX)]
		else:
			print('Low Confidence in faces detected.')
			return []

	@staticmethod
	def is_face_large_enough(face, h_size = 20, w_size = 20):
		(fH, fW) = face.shape[:2]
		return not(fW < h_size or fH < w_size)

	def extract_facial_features(self, image, tag):
		(h, w) = image.shape[:2]
		image_blob = cv2.dnn.blobFromImage(
			cv2.resize(image, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB = False, crop = False)
		detections = self.get_face_detections(image_blob)
		if len(detections) > 0:
			print("Have detected at least one face. Proceeding")
			facial_boundary = self.identify_facial_bounding_box(detections, h, w)
			if facial_boundary:
				face = image[facial_boundary[0][0]:facial_boundary[0][1], facial_boundary[1][0]:facial_boundary[1][1]]
				if self.is_face_large_enough(face):
					# bw_face = cv2.threshold(face, 128, 255, cv2.THRESH_BINARY)[1]
					cv2.imwrite("op/sample_faces/{}_{}.png".format(tag, self.counter), face)
					face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255,
													  (96, 96), (0, 0, 0), swapRB = True, crop = False)
					self.embedder.setInput(face_blob)
					return self.embedder.forward().flatten()
		return []

	def process_facial_feature_extraction(self, image, tag, insert_into_db):
		image = imutils.resize(image, width = 600)
		facial_features = self.extract_facial_features(image, tag)
		if len(facial_features) > 0:
			self.increase_counter()
			if insert_into_db:
				serialized_features = serialize_features(facial_features)
				run_query_noop(self.mysql_connector, insert_facial_features(tag, serialized_features))
				return True
			else:
				return facial_features
		return False
