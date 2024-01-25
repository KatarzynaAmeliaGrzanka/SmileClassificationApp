import os
import shutil


def divide_data(source_path, train_data_path, validation_data_path, test_data_path, train_t, val_t, test_t):
    ## Function for dividing data into train, validate and test folders
    # Input parameters:
    #   -source_path: string, path to directory where data is stored
    #   -train_data_path: string, path to directory where training data should be stored
    #   -validation_data_path: string, path to directory where validation data should be stored
    #   -test_data_path: string, path to directory where test data should be stored
    #   - train_t - threshold for training data
    #   - train_t - threshold for validation data
    #   - train_t - threshold for testing data

    if not os.path.exists(source_path):
        raise FileNotFoundError (f"Source directory not found")
    if not os.path.exists(train_data_path):
        raise FileNotFoundError (f"Train directory not found")
    if not os.path.exists(validation_data_path):
        raise FileNotFoundError (f"Validation directory not found")
    if not os.path.exists(test_t):
        raise FileNotFoundError (f"Test directory not found")
    
    try: 
        train_t = int(train_t)
    except ValueError:
        print("Invalid parameter train_t.")
        return
    try: 
        val_t = int(val_t)
    except ValueError:
        print("Invalid parameter val_t.")
        return
    try: 
        test_t = int(test_t)
    except ValueError:
        print("Invalid parameter test_t.")
        return

    if train_t < 0 or val_t < 0 or test_t < 0:
        print("Invalid parameters.")
        return

    count1 = 0
    count2 = 0
    count3 = 0
    count = 0
    for file in os.listdir(source_path):
        count += 1
        print("Moving image number: " + str(count))
        number = int(file[0:3])
        if number < train_t:
            count1 += 1
            from_directory = os.path.abspath(os.path.join(os.sep, source_path, file))
            to_directory = os.path.abspath(os.path.join(os.sep, train_data_path, file))

            if os.path.isfile(from_directory):
                shutil.copy(from_directory, to_directory)
            else:
                print("Error: " + from_directory + " is not a file. ")
        elif number < val_t:
            count2 += 1
            from_directory = os.path.abspath(os.path.join(os.sep, source_path, file))
            to_directory = os.path.abspath(os.path.join(os.sep, validation_data_path, file))

            if os.path.isfile(from_directory):
                shutil.copy(from_directory, to_directory)
            else:
                print("Error: " + from_directory + " is not a file. ")
        elif number <= test_t:
            count3 += 1
            from_directory = os.path.abspath(os.path.join(os.sep, source_path, file))
            to_directory = os.path.abspath(os.path.join(os.sep, test_data_path, file))

            if os.path.isfile(from_directory):
                shutil.copy(from_directory, to_directory)
            else:
                print("Error: " + from_directory + " is not a file. ")

    print("\nProcess done.\n") 
    print(str(count1) + " images were put in train directory. ")   
    print(str(count2) + " images were put in validation directory. ")   
    print(str(count3) + " images were put in test directory. ")           

def divide_into_spontaneous_and_deliberate_folders(source_path, deliberate_path, spontaneous_path):
     ## Function for dividing data into two folders (spontaneous and deliberate)
     #   -source_path: string, path to directory where data is stored
     #   -deliberate_path: string, path to directory where deliberate data should be stored
     #   -spontaneous_path: string, path to directory where spontaneous data should be stored

     if not os.path.exists(source_path):
        raise FileNotFoundError (f"Source directory not found")
     
     if not os.path.exists(deliberate_path):
        os.makedirs(deliberate_path)
     if not os.path.exists(spontaneous_path):
        os.makedirs(spontaneous_path)
     deliberate_count = 0
     spontaneous_count = 0
     for file in os.listdir(source_path):
        if 'deliberate' in file:
            from_directory = os.path.abspath(os.path.join(os.sep, source_path, file))
            to_directory = os.path.abspath(os.path.join(os.sep, deliberate_path, file))
            if os.path.isfile(from_directory):
                shutil.copy(from_directory, to_directory)
                deliberate_count += 1
            else:
                print("Error: " + from_directory + " is not a file. ")
        if 'spontaneous' in file:
            from_directory = os.path.abspath(os.path.join(os.sep, source_path, file))
            to_directory = os.path.abspath(os.path.join(os.sep, spontaneous_path, file))
            if os.path.isfile(from_directory):
                shutil.copy(from_directory, to_directory)
                spontaneous_count += 1
            else:
                print("Error: " + from_directory + " is not a file. ")
     print("\nProcess done. \n")
     print("Images with deliberate smiles: " + str(deliberate_count))
     print("Images with spontaneous smiles: " + str(spontaneous_count))

