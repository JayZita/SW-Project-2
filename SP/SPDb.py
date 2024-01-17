from SPDbEntry import SPDbEntry
import csv

class SPDb:

    def __init__(self, init=False, dbName='SPDb.csv'):
        # CSV filename         
        self.dbName = dbName
        # initialize container of database entries
        self.entries = []
        print('TODO: __init__')


    def fetch_characters(self):
        print('TODO: fetch_character')
        tupleList = []

        tupleList += [(entry.id, entry.name, entry.job, entry.level, entry.status) for entry in self.entries]

        return tupleList

    def insert_character(self, id, name, job, level, status):
        """
        - inserts an entry in the database
        - no return value
        """
        newEntry = SPDbEntry(id=id, name=name, job=job, level=level, status=status)
        self.entries.append(newEntry)
        print('TODO: insert_character')

    def delete_character(self, id):
        """
        - deletes the corresponding entry in the database as specified by 'id'
        - no return value
        """
        for entry in self.entries:
            if entry.id == id:
                self.entries.remove(entry)
                break
        print('TODO: delete_character')

    def update_character(self, new_name, new_job, new_level, new_status, id):
        """
        - updates the corresponding entry in the database as specified by 'id'
        - no return value
        """
        entry_found = False
        print(f"Updating entry with id {id} to: Name={new_name}, Job={new_job}, Level={new_level}, Status={new_status}")
        for entry in self.entries:
            if entry.id == id:
                entry.name = new_name
                entry.job = new_job
                entry.level = new_level
                entry.status = new_status
                entry_found = True
                break

        if not entry_found:
            raise ValueError(f"ID {id} does not exist in the database")
        print('Entry updated successfully')
     
              

    def export_csv(self):

        with open(self.dbName, 'w') as file:
            for entry in self.entries:
                file.write(f"{entry.id},{entry.name},{entry.job},{entry.level},{entry.status}\n")
        print('TODO: export_csv')

    def import_csv(self, csv_filename):
        try:
            if not csv_filename.lower().endswith('.csv'):
                csv_filename += '.csv'

            with open(csv_filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    id, name, job, level, status = row
                    # Add logic to handle the data, e.g., insert into your database
                    self.insert_character(id, name, job, level, status)
            print('Data imported successfully')
            return True
        except FileNotFoundError:
            print(f'Error importing data: File not found - {csv_filename}')
            return False
        except Exception as e:
            print(f'Error importing data: {e}')
            return False

    def id_exists(self, id):
        """
        - returns True if an entry exists for the specified 'id'
        - else returns False
        """
        return any(entry.id == id for entry in self.entries)