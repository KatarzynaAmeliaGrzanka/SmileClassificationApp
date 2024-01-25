import os
import cv2



def divide_into_frames(videos_dir, frames_dir, nb_of_frames_per_video, start_frame, period):
    ## Function for dividing a video into frames and saving them 
        # Input parameters:
        #   - videos_dir: a path to directory where videos are stored
        #   - frames_dir: a path to directory where frames are to be stored
        #   - nb_of_frames_per_video: how many frames to obtain from one video
        #   - start_frame: from what number frames are to be stored
        #   - period: parameter that makes possible skipping some frames (for example taking every other frame)
        # Result of a function:
        #   JPG files with frames from videos saved in frames_dir. 
    
    try: 
        start_frame = int(start_frame)
    except ValueError:
        print("Invalid parameter start_frame.")
        return
    
    try: 
        start_frame = int(nb_of_frames_per_video)
    except ValueError:
        print("Invalid parameter nb_of_frames_per_video.")
        return
    
    try: 
        start_frame = int(period)
    except ValueError:
        print("Invalid parameter period.")
        return
    
    if start_frame < 0 or nb_of_frames_per_video < 0 or period < 0:
        print("Invalid parameters.")
        return

    

    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    video_processed = 0
    frame_creation_errors = 0

    for filename in os.listdir(videos_dir):
       video_path = os.path.join(videos_dir, filename)
       if os.path.isfile(video_path):
            video_processed += 1
            print("Processing video: " + str(video_processed))
            video = cv2.VideoCapture(video_path)
            current_frame = 0
            while current_frame < start_frame:
                current_frame += 1
                success, frame = video.read()
            os.chdir(frames_dir)
            while current_frame < (start_frame + nb_of_frames_per_video * period):
                if current_frame % period != 0:
                    current_frame += 1
                    success, frame = video.read()
                else:
                    success, frame = video.read()
                    if success:
                        frame_name = f'{filename}_frame{str(current_frame)}.jpg'
                        cv2.imwrite(frame_name, frame)                           
                        current_frame += 1
                    else:
                        print("Error while reading frame number: " + str(current_frame) + " from video: " + str(filename))
                        current_frame += 1
                        frame_creation_errors += 1
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
