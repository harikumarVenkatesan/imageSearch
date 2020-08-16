import mysql.connector
import pandas as pd


def get_conn(user, pwd, auth_plugin = 'mysql_native_password'):
	return mysql.connector.connect(
		host = "localhost",
		user = user,
		password = pwd,
		auth_plugin = auth_plugin
	)


def run_query_noop(mysql_connector, query):
	cursor = mysql_connector.cursor()
	cursor.execute(query)
	mysql_connector.commit()
	cursor.close()
	return


def run_query_op(mysql_connector, query):
	return pd.read_sql(query, mysql_connector)
