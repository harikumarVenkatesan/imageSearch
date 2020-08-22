import numpy as np
import pickle


def get_file_format(path):
	extension = path.split(".")[-1]
	return extension


def get_image_central_measures(image):
	(h, w) = image.shape[:2]
	(cX, cY) = (int(w * 0.5), int(h * 0.5))
	return h, w, cX, cY


def serialize_features(features):
	return ",".join(map(str, features))


def deserialize_features(feature_list, dtype = "float32"):
	return np.asarray(feature_list.split(","), dtype = dtype)


def pickle_dump(path, obj):
	with open(path, "wb") as f:
		f.write(pickle.dumps(obj))
	return True


