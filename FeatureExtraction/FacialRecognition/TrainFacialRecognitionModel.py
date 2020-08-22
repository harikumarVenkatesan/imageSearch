# USAGE
# python train_model.py --embeddings output/embeddings.pickle \
#	--recognizer output/recognizer.pickle --le output/le.pickle

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from HelperFunctions.MysqlConnector import run_query_op
from HelperFunctions.HelperFunctions import pickle_dump, deserialize_features
from FeatureExtraction.SqlQueries import get_labeled_facial_data


class TrainFacialRecognitionModel:
	def __init__(self, mysql_connector):
		self.mysql_connector = mysql_connector
		self.labeled_data = None
		self.labels = None
		self.label_encoder = None
		self.recognizer = None
		self.get_labeled_data()

	def get_labeled_data(self):
		df = run_query_op(self.mysql_connector, get_labeled_facial_data())
		df['features'] = df["features"].apply(deserialize_features)
		self.labeled_data = df
		print(df.head())
		return

	def transform_labels(self):
		label_encoder = LabelEncoder()
		labels = label_encoder.fit_transform(self.labeled_data["name"])
		self.labels, self.label_encoder = labels, label_encoder
		return

	def train_SVM(self):
		self.transform_labels()
		recognizer = SVC(C=1.0, kernel="linear", probability=True)
		print(type(self.labeled_data["features"]))
		recognizer.fit(self.labeled_data["features"].tolist(), self.labels)
		self.recognizer = recognizer
		print("Training Done", recognizer)

	def train_ml_model(self, model_name: str, persist_in_disk):
		if model_name.lower() == "svm":
			self.train_SVM()

		if persist_in_disk:
			# write the actual face recognition model to disk
			pickle_dump(persist_in_disk['model_path'], self.recognizer)
			pickle_dump(persist_in_disk['label_encoder_path'], self.label_encoder)
			return True
		return self.recognizer, self.label_encoder
