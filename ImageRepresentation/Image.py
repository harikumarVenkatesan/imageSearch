from HelperFunctions.mysqlConnector import get_conn, run_query_noop, run_query_op
from HelperFunctions.helperFunctions import get_file_format
from ImageRepresentation.queries import insert_image_path_query, get_image_id_query, has_feature_extracted_query
import pandas as pd  # move this later to Connector Class
import os
from mysql.connector.errors import IntegrityError
import cv2


class Image(object):
    def __init__(self, path, mysql_connector):
        self.path = path
        self.image_format = get_file_format(path)
        self.mysql_connector = mysql_connector
        self.image_id = self.get_image_id()
        self.image = cv2.imread(self.path)
        self.has_color_descriptor = self.has_color_descriptor_feature_extracted()

    def has_color_descriptor_feature_extracted(self):
        count = run_query_op(self.mysql_connector,
                             has_feature_extracted_query(self.image_id, "image_search.color_descriptor_features"))['cnt'].iloc[0]
        return True if count > 0 else False

    def get_image_id(self):
        """
            Get Image ID for a given path.
            Image Table, (image_search.image) is defined with auto_increment which is used as ID,
            and has a UNIQUE on the image path column. If the insert fails,
            then it's assumed to be because image_path exists
        """
        try:
            run_query_noop(self.mysql_connector, insert_image_path_query(self.path, self.image_format))
        except IntegrityError:
            pass
        image_id = run_query_op(self.mysql_connector, get_image_id_query(self.path))['image_id'].iloc[0]
        return image_id

    def __str__(self):
        return self.path + "__" + str(self.image_id)
