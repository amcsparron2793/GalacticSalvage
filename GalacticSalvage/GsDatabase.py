from pathlib import Path

from SQLLite3HelperClass import SQLlite3Helper

class GsDatabase(SQLlite3Helper):
    """
    This class represents a wrapper for a SQLite database, extending the `SQLlite3Helper` class.
    It provides methods to create tables and initialize a new database.

    Attributes:
        CREATE_TABLES_LOCATION (Path):
            A `Path` object representing the location of the SQL file containing the table creation statements.

    Methods:
        __init__(db_file_path: str): Initializes a new instance of the `GsDatabase` class.

        _create_statements(): Parses the SQL file and returns a list of individual table creation statements.

        initialize_new_db(): Executes the table creation statements to initialize a new database.

    Usage:
        db = GsDatabase('path/to/db_file.db')
        db.initialize_new_db()

    Note: This documentation does not include example code or usage examples.
    """
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
        for t in self._create_statements_list:
            self.csr.execute(t)
            self.cxn.commit()

