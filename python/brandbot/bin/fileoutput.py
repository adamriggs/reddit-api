import MySQLdb

db = MySQLdb.connect(host="localhost", user="*****",passwd="*****",db="reddit") 
cur = db.cursor()
f = open('db-output.txt','w')

cur.execute('SELECT * FROM brandbot')
mysql_rows=cur.fetchall()

for mysql_row in mysql_rows:
	f.write(mysql_row[3]+"\n")
	f.write(mysql_row[5]+"\n")
	f.write(mysql_row[6]+"\n")
	f.write(mysql_row[8]+"\n")
	f.write("\n\n\n")
