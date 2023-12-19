import dlib
import os
import cv2
import numpy as np

def landmarks_to_np(shape, dtype='int'):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

FACIAL_LANDMARKS_IDXS = {
    'left_eye': (42, 48),   # Indices for the left eye landmarks
    'right_eye': (36, 42),  # Indices for the right eye landmarks
    # ... other facial landmarks if needed
}

def align_face(image_path, dest_path):
    image = cv2.imread(image_path)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp/SmileClassificationApp/shape_predictor_68_face_landmarks.dat")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    error = 0
    rects = detector(gray)
    for rect in rects:
        shape = predictor(gray, rect)

        #for n in range(0, 68):
          #  x = shape.part(n).x
          #  y = shape.part(n).y
           #   cv2.circle(image, (x, y), 4, (255, 0, 0), -1)
        
        #cv2.imwrite("C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test/before_rotation.jpg", image)
        #cv2.imshow("Image", image)
        #cv2.waitKey(0)
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
        #cv2.imshow("Rotated Image", rotated_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        cv2.imwrite(dest_path, rotated_image)
    return (error)
#align_face('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test/001_spontaneous_smile_22.mp4_frame72.jpg')

def align_faces_in_dir(source_path, destination_path):
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


align_faces_in_dir('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/faces', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/aligned_faces'           )

#align_faces_in_dir('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test')