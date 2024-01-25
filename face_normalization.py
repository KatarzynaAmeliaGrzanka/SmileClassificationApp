import dlib
import os
import cv2
import numpy as np


def landmarks_to_np(shape, dtype='int'):
    # Function to store face landmarks in a numpy array
    # input: face detected with shape_predictor from dloib library
    # output: numpy array with coordinates of 68 facial landmarks
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


# Dictionary for storing points that represent eyes in 68 dlib landmarks
FACIAL_LANDMARKS_IDXS = {
    'left_eye': (42, 48),   # Indices for the left eye landmarks
    'right_eye': (36, 42),  # Indices for the right eye landmarks
}


def align_face(image_path, dest_path):
    ## Function to align faces on an image 
        # input:
        #  -image_path : string, a path to an image to be aligned
        #  -dest_path : string, a path were an aligned image should be stored
    image = cv2.imread(image_path)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp/SmileClassificationApp/shape_predictor_68_face_landmarks.dat")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    error = 0

    rects = detector(gray)
    for rect in rects:
        shape = predictor(gray, rect)

    if len(rects) == 0:
        error = 1
    else:
        shape = landmarks_to_np(shape)
        (left_eye_beg, left_eye_end) = FACIAL_LANDMARKS_IDXS['left_eye']    
        (right_eye_beg, right_eye_end) = FACIAL_LANDMARKS_IDXS['right_eye']

        left_eye_landmarks = shape[left_eye_beg:left_eye_end]
        right_eye_landmarks = shape[right_eye_beg:right_eye_end]

        left_eye_center = left_eye_landmarks.mean(axis=0).astype('int')
        right_eye_center = right_eye_landmarks.mean(axis=0).astype('int')

        dY = right_eye_center[1] - left_eye_center[1]
        dX = right_eye_center[0] - left_eye_center[0]


        angle = np.degrees(np.arctan2(dY, dX))
        angle = angle - 180

        matrix = cv2.getRotationMatrix2D((image.shape[1] // 2, image.shape[0] // 2), angle, 1)

        rotated_image = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC)


        cv2.imwrite(dest_path, rotated_image)
    return (error)


def align_faces_in_dir(source_path, destination_path):
    ## Function for aligning all images in a given directory
    #  - source_path : a path to directory where images are stored
    #  - destination_path : a path were aligned images are supposed to be saved
     
     if not os.path.exists(source_path):
        raise FileNotFoundError (f"Source directory not found")

     if not os.path.exists(destination_path):
        raise FileNotFoundError (f"Destination directory not found")


     rotation_count = 0
     error_count = 0
     for file in os.listdir(source_path):
        print("Aligning face number: "+ str(rotation_count))
        image_path = os.path.abspath(os.path.join(os.sep, source_path, file))
        dest_path = os.path.abspath(os.path.join(os.sep, destination_path, file))
        check = align_face(image_path, dest_path)
        if check:
            print("Error occured. ")
            error_count += 1
        else:
            rotation_count += 1

     print("\n\nProcess done.")
     print("\nAligned " + str(rotation_count) + ' images\n')
     print("\nNumber of errors: " + str(error_count))


