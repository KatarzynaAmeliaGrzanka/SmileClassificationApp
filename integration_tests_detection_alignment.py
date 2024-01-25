import os
from face_detection import detect_faces_in_directory
from face_normalization import align_face, align_faces_in_dir


def test_images_in_dest_dir():
        face_detect_source_dir = "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/integration_tests_data/test1/detect_source"
        face_detect_dest_dir = "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/integration_tests_data/test1/detect_destination"
        face_align_dest_dir = "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/integration_tests_data/test1/align_destination"

        detect_faces_in_directory(face_detect_source_dir, face_detect_dest_dir)
        align_faces_in_dir(face_detect_dest_dir, face_align_dest_dir)

        if any(os.scandir(face_align_dest_dir)):
            print("Test test_images_in_dest_dir passed.")
        else:
            print("Test test_images_in_dest_dir failed.")


def test_number_of_images_in_dest_folder():
    face_detect_source_dir = "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/integration_tests_data/test2/detect_source"
    face_detect_dest_dir = "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/integration_tests_data/test2/detect_destination"
    face_align_dest_dir = "C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/integration_tests_data/test2/align_destination"

    source_count = 0
    dest_count = 0

    detect_faces_in_directory(face_detect_source_dir, face_detect_dest_dir)
    align_faces_in_dir(face_detect_dest_dir, face_align_dest_dir)
    
    for file in os.listdir(face_detect_source_dir):
         source_count += 1

    for file in os.listdir(face_detect_source_dir):
         dest_count += 1

    if(source_count == dest_count):
         print("Test test_number_of_images_in_dest_folder passed. ")
    else:
       print("Test test_number_of_images_in_dest_folder failed. ")  


test_number_of_images_in_dest_folder()