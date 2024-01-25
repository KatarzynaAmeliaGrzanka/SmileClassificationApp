import unittest
import os
from face_normalization import align_face, align_faces_in_dir
import pathlib as pl

class UnitTestDetectFaces(unittest.TestCase):
    def test_not_existing_source_dir(self):
        with self.assertRaises(FileNotFoundError):
            align_faces_in_dir("non-existing-directory", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/existing_directory")

    def test_not_existing_destination_dir(self):
        with self.assertRaises(FileNotFoundError):
            align_faces_in_dir("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/existing_directory", "non-existing-directory")

    def test_new_image_in_destination_dir(self):
        align_faces_in_dir("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/align_source_1", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/align_destination_1")
        self.assertTrue(os.listdir("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/align_destination_1"))

    def test_no_face_on_image(self):
         with self.assertRaises(IOError):
            align_faces_in_dir("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/align_source_2", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/align_destination_2")

    def test_not_image(self):
        test = align_face("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/align_source_3/not-image.txt", "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/unit-tests-data/align_destination_2/not-image.jpg")
        self.assertEqual(test,1)

if __name__ == '__main__':
    unittest.main()