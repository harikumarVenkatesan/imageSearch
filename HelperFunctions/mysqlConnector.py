import mysql.connector


def get_conn(user, pwd, auth_plugin = 'mysql_native_password'):
	return mysql.connector.connect(
		host = "localhost",
		user = user,
		password = pwd,
		auth_plugin = auth_plugin
	)
