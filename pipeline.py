import frames_from_videos
import face_detection
import face_normalization
import data_prep
import tensorflow as tf
import numpy as np

videos_directory = ""
frames_directory = ""
faces_directory = ""
aligned_faces_directory = ""
train_data_directory = ""
validation_data_directory = ""
test_data_directory = ""


frames_from_videos.divide_into_frames(videos_directory, frames_directory, 60, 10, 2)
face_detection.detect_faces_in_directory(frames_directory, faces_directory)
face_normalization.align_faces_in_dir(faces_directory, aligned_faces_directory)


data_prep.divide_data(aligned_faces_directory, 
            train_data_directory, 
            validation_data_directory,
            test_data_directory,
            410, 515, 564)

data_prep.divide_into_spontaneous_and_deliberate_folders(train_data_directory, '', '')
data_prep.divide_into_spontaneous_and_deliberate_folders(validation_data_directory, '', '')
data_prep.divide_into_spontaneous_and_deliberate_folders(test_data_directory, '', '')