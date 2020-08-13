from HelperFunctions.mysqlConnector import get_conn
from ImageRepresentation.queries import insert_image_path_query, get_image_id_query
import pandas as pd  # move this later to Connector Class
import os
from mysql.connector.errors import IntegrityError


class Image(object):
    def __init__(self, path):
        self.path = path
        self.mysql_connector = get_conn(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PWD"))
        self.image_id = self.get_image_id()

    def get_image_id(self):
        """
            Get Image ID for a given path.
            Image Table, (image_search.image) is defined with auto_increment which is used as ID,
            and has a UNIQUE on the image path column. If the insert fails,
            then it's assumed to be because image_path exists
        """
        try:
            self.mysql_connector.cursor().execute(insert_image_path_query(self.path))
            self.mysql_connector.commit()
        except IntegrityError:
            pass
        image_id = pd.read_sql(get_image_id_query(self.path), self.mysql_connector)['image_id'].iloc[0]
        return image_id

    def __str__(self):
        return self.path + "__" + str(self.image_id)

