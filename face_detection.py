import cv2
import os

## Function for detecting and cutting faces from images in a directory.
# Input parameters:
#   - dir_pat: a path to a directory where the images are stored.
#   - destination_path: a path to a destination directory where faces are to be stored.
# Output:
#   Faces cut from images in dir_path are saved in destination_path ( as jpg images ).

def detect_faces_in_directory(dir_path, destination_path):
    # load and store a file for face detection as face_cascade
    face_cascade = cv2.CascadeClassifier('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp/SmileClassificationApp/haarcascade_frontalface_alt.xml')
    # a variable for storing the number of detected faces on all images
    faces_count = 0
    for file in os.listdir(dir_path):
        print("Detecting face number: " + str(faces_count))
        image_path = os.path.abspath(os.path.join(os.sep, dir_path, file))
        dest_path = os.path.abspath(os.path.join(os.sep, destination_path, file))
        if not os.path.exists(image_path):
            print("Error: incorrect path: " + str(image_path))
        else:
            # read an image from which faces are to be detected
            image = cv2.imread(image_path)
            if image is None:
                print("Error while reading a file: " + str(image_path))
            else:
                # convert to gray scale image
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # detect and store faces
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                # w, y, w, h are coordinates stored for every face detected
                for (x, y, w, h) in faces:
                    # draw a rectangle around a face detected
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    # cut image to a size of a rectangle where face is detected
                    faces = image[y:y + h, x:x + w]
                    # write obtained image to a destination folder
                    cv2.imwrite(dest_path, faces)
                    faces_count += 1
    print("\n\nProcess done.\n")
    print("Number of faces detected: ")
    print(faces_count)
        

detect_faces_in_directory('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/frames', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/faces')