from HelperFunctions.mysqlConnector import get_conn

class Image(object):
    def __init__(self, path):
        self.path = path
        self.image_id = self.get_image_ID()

    def get_image_ID(self):


