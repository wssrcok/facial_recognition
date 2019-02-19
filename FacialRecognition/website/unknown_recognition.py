import face_recognition
import os
import pickle
from FacialRecognition.settings import DEBUG

def get_encoding(file):
    try:
        img_np = face_recognition.load_image_file(file)
    except IOError:
        print(file + "is not an image file.")
    try:
        encoding = face_recognition.face_encodings(img_np,num_jitters=3)[0]
        return encoding
    except IndexError:
        print("No face detected in " + file)


def retrive_photos(
    tolerance,
    input_img,
    known_encodings,
    known_person_dir="website/static/images"):
    unknown_encoding = get_encoding(input_img)
    known_filenames = os.listdir(known_person_dir)
    
    retrived_file_paths = []
    for img_index in range(len(known_encodings)):
        if known_encodings[img_index] is None:
            continue
        distances = face_recognition.face_distance(known_encodings[img_index], unknown_encoding)
        for distance in distances:
            if distance < tolerance:
                filename = known_filenames[img_index]
                retrived_file_paths.append(filename)
                if DEBUG:
                    print(filename+", distance:", distance)
    return retrived_file_paths

def recognition_main(unknown_person_path, tolerance):
    with open('website/static/encodings.txt', 'rb') as f:
        known_encodings = pickle.load(f)
        return retrive_photos(
            tolerance,
            unknown_person_path,
            known_encodings, 
            known_person_dir="website/static/images")

