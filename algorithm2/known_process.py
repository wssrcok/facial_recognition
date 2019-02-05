import face_recognition
import os
import pickle


def get_encoding(file):
    try:
        img_np = face_recognition.load_image_file(file)
    except OSError:
        print(file + "is not an image file.")
    try:
        encoding = face_recognition.face_encodings(img_np,num_jitters=3)
        return encoding
    except IndexError:
        print("No face detected in " + file)


def get_face_list(known_person_dir = "./known_person"):
    known_encodings = []

    for img in os.listdir(known_person_dir):
        img_path = os.path.join(known_person_dir, img)
        img_encoding = get_encoding(img_path)
        known_encodings.append(img_encoding)
        print(img + ": " + str(len(img_encoding)) + " face(s) detected. ")

    return known_encodings
               

if __name__ == '__main__':
    
    known_encodings = get_face_list(known_person_dir="./known_person")
    print(len(known_encodings))
    with open("encodings.txt", 'wb') as f:
        pickle.dump(known_encodings, f)

