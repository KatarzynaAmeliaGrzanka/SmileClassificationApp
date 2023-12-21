import os
import shutil


def divide_data(source_path, train_data_path, validation_data_path, test_data_path, train_t, val_t, test_t):
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

#divide_data('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/aligned_faces', 
#            'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/train_data', 
#            'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/validation_data',
#            'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test_data',
#            410, 515, 564)

#print("Test folder.")
#divide_into_spontaneous_and_deliberate_folders('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test_data', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test_data/deliberate', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/test_data/spontaneous' )
#print("Validation folder.")
#divide_into_spontaneous_and_deliberate_folders('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/validation_data', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/validation_data/deliberate', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/validation_data/spontaneous' )
print("Train folder.")
divide_into_spontaneous_and_deliberate_folders('C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/train_data', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/train_data/deliberate', 'C:/Users/pazie/Documents/Computer Science/SmileClassificationApp_data/train_data/spontaneous' )
