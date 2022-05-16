import unittest
import os
from PyQt5 import QtCore

from utils.sql_operations import create_connection, create_table, sql_create_annotations_table, create_annotation
from dataset import ImageAnnotationsDataset
from explore_annotations_window import ExploreAnnotationsWindow
from utils.annotation import Annotation

TEST_IMAGE = "testimage.jpg"

class TestAnnotate(unittest.TestCase):
    def setUp(self):
        self.db = create_connection("../tests/testdatabase.db")
        create_table(self.db, sql_create_annotations_table)

    def tearDown(self):
        os.remove("testdatabase.db")
        
    def test_negative_coords(self):
        annotation = Annotation(QtCore.QPoint(-100,100), QtCore.QPoint(200,200), TEST_IMAGE, "Dob")
        
        ds = ImageAnnotationsDataset("test_images/", testing=True)
        self.assertEqual(len(ds), 0, "Annotation with faulty coordinates is included")
  
if __name__ == '__main__':
    unittest.main()