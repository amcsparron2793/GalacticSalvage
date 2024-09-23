from pathlib import Path

from SQLLite3HelperClass import SQLlite3Helper

class GsDatabase(SQLlite3Helper):
    def __init__(self, db_file_path: str):
        super().__init__(db_file_path)
        if Path(self.db_file_path).is_file():
            self.new_db = True
        else:
            self.new_db = False
        self.GetConnectionAndCursor()
        if self.new_db:
            self.initialize_new_db()

    def initialize_new_db(self):
        # TODO: run the CreateTables.sql statements
        pass
