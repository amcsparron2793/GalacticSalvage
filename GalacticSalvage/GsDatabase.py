from pathlib import Path

from SQLLite3HelperClass import SQLlite3Helper

class GsDatabase(SQLlite3Helper):
    CREATE_TABLES_LOCATION = Path('../Misc_Project_Files/CreateTables.sql').resolve()

    def __init__(self, db_file_path: str):
        super().__init__(db_file_path)
        self._create_statements_list = self._create_statements()
        if Path(self.db_file_path).is_file():
            self.new_db = False
        else:
            self.new_db = True
        self.cxn, self.csr = self.GetConnectionAndCursor()
        if self.new_db:
            self.initialize_new_db()

    def _create_statements(self):
        with open(self.CREATE_TABLES_LOCATION, 'r') as f:
            full_file = f.read()
        return full_file.split(';')

    def initialize_new_db(self):
        # TODO: run the CreateTables.sql statements
        for t in self._create_statements_list:
            self.csr.execute(t)
            self.cxn.commit()

