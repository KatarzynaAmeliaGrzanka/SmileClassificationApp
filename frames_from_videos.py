# import OS module
import os
#import OpenCV librart
import cv2

# save path to a directory for frames cut from videos
frames_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/frames'
# save path to a directory where are videos from a database
videos_directory = 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/videos'

## Function for dividing a video into frames and storing them
# Input parameters:
#   - videos_dir: a path to directory where videos are stored
#   - frames_dir: a path to directory where frames are to be stored
#   - nb_of_frames_per_video: how many frames to obtain from one video
#   - start_frame: from what number frames are to be stored
#   - period: parameter that makes possible skipping some frames 
# Output:
#   JPG files with frames from videos. 

def divide_into_frames(videos_dir, frames_dir, nb_of_frames_per_video, start_frame, period):
    # it it doesn't already exists, create a directory for storing frames
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    # variable for storing information how many videos has already been processed
    video_processed = 0
    # variable for storing number of errors obtained with creating the frames
    frame_creation_errors = 0

    # for every video file in the video directory
    for filename in os.listdir(videos_dir):
       # obtain a path to a video file
       video_path = os.path.join(videos_dir, filename)
       if os.path.isfile(video_path):
            #increment video_processed variable
            video_processed += 1
            print("Processing video: " + str(video_processed))
            # start processing the video
            video = cv2.VideoCapture(video_path)
            # variable for storing the number of frame processed
            current_frame = 0
            # skip some number of frames (start_frame)
            while current_frame < start_frame:
                current_frame += 1
                success, frame = video.read()
            # move to directory where frames will be stored
            os.chdir(frames_dir)
            # process next frames
            while current_frame < (start_frame + nb_of_frames_per_video * period):
                # if frame number is not divided by period, it is skipped
                if current_frame % period != 0:
                    current_frame += 1
                    success, frame = video.read()
                else:
                    # store information about the success of capturing the frame and the frame
                    success, frame = video.read()
                    if success:
                        # save frame image
                        frame_name = f'{filename}_frame{str(current_frame)}.jpg'
                        cv2.imwrite(frame_name, frame)                           
                        current_frame += 1
                    else:
                        # in case error occures
                        print("Error while reading frame number: " + str(current_frame) + " from video: " + str(filename))
                        current_frame += 1
                        frame_creation_errors += 1
            # end processing of the video
            video.release()
            cv2.destroyAllWindows()
            print("Video processed successfully.")
    # display summary
    print("\n\nProcess done. \n")
    print("Number of videos processed:")
    print(video_processed)
    print("\nNumber of frames created: ")
    print(nb_of_frames_per_video * video_processed - frame_creation_errors)   
    print("\nNumber of error occurences: ")  
    print(frame_creation_errors)   

# call function
divide_into_frames(videos_directory, frames_directory, 10, 60, 2)