# Python libraries
import os
import sys
from PyQt5.QtWidgets import QApplication

# Relative imports
from gui import GUI
from utils.sql_operations import create_connection, create_table, sql_create_annotations_table

# Where to create or where is you db located
DATABASE_PATH = "../../database.db"

def main():
    # Every Qt application must have one instance of QApplication.
    global app # Use global to prevent crashing on exit
    app = QApplication(sys.argv)

    # Make sure the directory structure is correct
    if not os.path.exists('../../images/annotated'):
        os.makedirs('../../images/annotated')
    if not os.path.exists('../../images/not_annotated'):
        os.makedirs('../../images/not_annotated')
        
    # Connect to the sql database
    db = create_connection(DATABASE_PATH)

    if db is not None:
        # Create the necessary tables if not yet created
        create_table(db, sql_create_annotations_table)
        # Create the qt widgets and windows
        gui = GUI(db)
        # Start the Qt event loop. (i.e. make it possible to interact with the gui)
        sys.exit(app.exec_())
    else:
        print("Error! Cannot create database connection.")
    

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

