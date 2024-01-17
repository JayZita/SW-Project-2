'''
This is the interface to an SQLite Database
'''

import sqlite3

class SPDbSqlite:
    def __init__(self, dbName='Characters.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                id TEXT PRIMARY KEY,
                name TEXT,
                role TEXT,
                level TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Employees (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    role TEXT,
                    level TEXT,
                    status TEXT)''')
        self.commit_close()

    def fetch_characters(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Characters')
        characters =self.cursor.fetchall()
        self.conn.close()
        return characters

    def insert_character(self, id, name, job, level, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Employees (id, name, role, level, status) VALUES (?, ?, ?, ?, ?)',
                    (id, name, job, level, status))
        self.commit_close()

    def delete_character(self, id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Employees WHERE id = ?', (id,))
        self.commit_close()

    def update_character(self, new_name, new_job, new_level, new_status, id):
        self.connect_cursor()
        self.cursor.execute('UPDATE Employees SET name = ?, role = ?, level = ?, status = ? WHERE id = ?',
                    (new_name, new_job, new_level, new_status, id))
        self.commit_close()

    def id_exists(self, id):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Employees WHERE id = ?', (id,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_employees()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

def test_SPDb():
    iSPDb = SPDbSqlite(dbName='SPDbSql.db')

    for entry in range(30):
        iSPDb.insert_character(entry, f'Name{entry} Surname{entry}', f'Swordsman {entry}', '45', 'Finding Quest')
        assert iSPDb.id_exists(entry)

    all_entries = iSPDb.fetch_characters()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iSPDb.update_character(f'Name{entry} Surname{entry}', f'Swordsman {entry}', '45', 'Finding Quest', entry)
        assert iSPDb.id_exists(entry)

    all_entries = iSPDb.fetch_characters()
    assert len(all_entries) == 30

    for entry in range(10):
        iSPDb.delete_character(entry)
        assert not iSPDb.id_exists(entry) 

    all_entries = iSPDb.fetch_characters()
    assert len(all_entries) == 20