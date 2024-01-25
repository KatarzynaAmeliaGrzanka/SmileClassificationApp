import unittest
import os
from face_detection import detect_faces_in_directory
import pathlib as pl

class UnitTestDetectFaces(unittest.TestCase):
    def test_not_existing_source_dir(self):
        with self.assertRaises(FileNotFoundError):
            detect_faces_in_directory("non-existing-directory", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/existing_directory")

    def test_not_existing_destination_dir(self):
        with self.assertRaises(FileNotFoundError):
            detect_faces_in_directory("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/existing_directory", "non-existing-directory")

    def test_new_image_in_destination_dir(self):
        detect_faces_in_directory("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/source2", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/destination2")
        self.assertTrue(os.listdir("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/destination2"))

    def test_image_path_exists(self):
        with self.assertRaises(IOError):
            detect_faces_in_directory("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/source", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/destination")

    def test_not_image_in_source_file(self):
        with self.assertRaises(IOError):
            detect_faces_in_directory("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/source3", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/destination3")

    def test_faces_count(self):
        faces_count = detect_faces_in_directory("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/source4", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/destination4")
        expected_faces_count = 5
        self.assertEqual(faces_count, expected_faces_count)

if __name__ == '__main__':
    unittest.main()