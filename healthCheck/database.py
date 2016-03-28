import MySQLdb

def machine_ip(username, password, project_name, service_name):
	db = MySQLdb.connect(config.database_url, username, password, username)
	cursor = db.cursor()
	cursor.execute("select machine from service where name = '%s' and project = '%s'" % (service_name, project_name))
	data = cursor.fetchone()
	#print project_name
	#print service_name
	#print data
	if data == None:
		db.close()
		return '-'
	else:
		cursor.execute("select ip from machine where id = %s" % data[0])
		data = cursor.fetchone()
		db.close()
		return data[0]
