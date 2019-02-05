import face_recognition
import os
import pickle

from PIL import Image

def get_encoding(file):
    try:
        img_np = face_recognition.load_image_file(file)
    except OSError:
        print(file + "is not an image file.")
    try:
        encoding = face_recognition.face_encodings(img_np,num_jitters=3)[0]
        return encoding
    except IndexError:
        print("No face detected in " + file)


def retrive_photos(
    known_encodings,
    known_person_dir="./known_person"):
    
    input_img = raw_input("Please enter the path of image of unknown person: ")
    unknown_encoding = get_encoding(input_img)
    
    for img_index in range(len(known_encodings)):
        distances = face_recognition.face_distance(known_encodings[img_index], unknown_encoding)
        
        for distance in distances:
            if distance < 0.4:
                # print(os.listdir(known_person_dir)[img_index])
                path = os.path.join(known_person_dir, os.listdir(known_person_dir)[img_index])
                im = Image.open(path)
                im.show()
               
        

if __name__ == '__main__':

    with open('encodings.txt', 'rb') as f:
        known_encodings = pickle.load(f)
   
    while True:
        try:
            retrive_photos(
                   known_encodings, 
                   known_person_dir="./known_person")
        except KeyboardInterrupt:
            print("")
            quit()
        
