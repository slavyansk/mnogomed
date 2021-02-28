import sqlite3

class Database:
	def __init__(self, db):
		self.conn = sqlite3.connect(db)
		self.cur = self.conn.cursor()
		self.cur.execute("""CREATE TABLE IF NOT EXISTS list_of_patients (id_p INTEGER PRIMARY KEY, studydate TEXT, name TEXT, birthday TEXT, p_sex TEXT, examination TEXT, report TEXT)""")
		self.conn.commit()
	
	def fetch(self):
		self.cur.execute("SELECT * FROM list_of_patients")
		rows = self.cur.fetchall()
		return rows
	
	def insert(self, studydate, name, birthday, p_sex, examination, report):
		self.cur.execute("INSERT INTO list_of_patients (studydate, name, birthday, p_sex, examination, report) VALUES(?,?,?,?,?,?)", (studydate, name, birthday, p_sex, examination, report))
		self.conn.commit()
	
	def remove(self, id_p):
		self.cur.execute("DELETE FROM list_of_patients WHERE id_p=?", (id_p,))
		self.conn.commit()
		
	def update(self, id_p, studydate, name, birthday, p_sex, examination, report):
		self.cur.execute("UPDATE list_of_patients SET studydate =?, name=?, birthday=?, p_sex=?, examination=?, report=? WHERE id_p=?",(studydate, name, birthday, p_sex, examination, report, id_p))
		self.conn.commit()

	def __del__(self):
		self.conn.close()
		
#db = Database('my_db.db')

