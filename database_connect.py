import pymysql
con = pymysql.connect(host='localhost', user='root', password='krishnendu@2003', database='project')
mycursor = con.cursor()