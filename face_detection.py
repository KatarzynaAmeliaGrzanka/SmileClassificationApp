import cv2
import os
import sys


def detect_faces_in_directory(dir_path, destination_path):
    ## Function for detecting and cutting faces from images in a directory.
        # Input parameters:
        #   - dir_pat: string, a path to a directory where the images are stored.
        #   - destination_path: string, a path to a destination directory where faces are to be stored.
        # Output:
        #   Faces cut from images in dir_path are saved in destination_path ( as jpg images ).
    
    if not os.path.exists(dir_path):
        raise FileNotFoundError (f"Source directory not found")

    if not os.path.exists(destination_path):
        raise FileNotFoundError (f"Destination directory not found")

    face_cascade = cv2.CascadeClassifier('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp/SmileClassificationApp/haarcascade_frontalface_alt.xml')
    faces_count = 0
    for file in os.listdir(dir_path):
        print("Detecting face number: " + str(faces_count))
        image_path = os.path.abspath(os.path.join(os.sep, dir_path, file))
        dest_path = os.path.abspath(os.path.join(os.sep, destination_path, file))
        if not os.path.exists(image_path):
            print("Error: incorrect path: " + str(image_path))
        else:
            image = cv2.imread(image_path)
            if image is None:
                print("Error while reading a file: " + str(image_path))
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    faces = image[y:y + h, x:x + w]
                    cv2.imwrite(dest_path, faces)
                    faces_count += 1
    print("\n\nProcess done.\n")
    print("Number of faces detected: ")
    print(faces_count)
    return faces_count
        

