import face_recognition
import os
import numpy as np
from tqdm import tqdm
import argparse
from PIL import Image

def get_encoding(dir):
	# Load the jpg files into numpy arrays
	img_np = face_recognition.load_image_file(dir)
	try:
		# Get the face encodings for each face in each image file
		# Since there could be more than one face in each image, it returns a list of encodings.
		# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
		encoding = face_recognition.face_encodings(img_np,num_jitters=3)[0]
	except IndexError:
		print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
		quit()
	return encoding

def get_face_list(known_person_dir = "./known_person"):
	duanwei_encoding = get_encoding("known_person/duan,wei.jpg")
	# known_faces_encoding only store one image per person, while known_faces stores all images
	known_faces_encoding = [duanwei_encoding]
	known_faces = [["duan,wei.jpg"]]
	for img in tqdm(os.listdir(known_person_dir)):
		img_dir = os.path.join(known_person_dir, img)
		img_encoding = get_encoding(img_dir)

		result = face_recognition.compare_faces(known_faces_encoding, img_encoding, tolerance=0.4)
		if True in result:
			index = np.where(np.array(result) == True)[0] # this returns [0,1,3] for nparray [True, True, False, True]
			for i in index:
				known_faces[i].append(img)
		else:
			known_faces_encoding.append(img_encoding)
			known_faces.append([img])
	for l in known_faces:
		print(l)
	return known_faces, known_faces_encoding

def retrive_photos(#input_img, 
				   known_faces, 
				   known_faces_encoding, 
				   known_person_dir="./known_person"):
	while(True):
		input_img = input("directory of input image? ")
		input_encoding = get_encoding(input_img)
		result = face_recognition.compare_faces(known_faces_encoding, input_encoding, tolerance=0.45)
		if True in result:
				index = np.where(np.array(result) == True)[0] # this returns [0,1,3] for nparray [True, True, False, True]
				for i in index: # for all lists that matches person's face
					for d in known_faces[i]:
						path = os.path.join(known_person_dir, d)
						im = Image.open(path)
						im.show()
		else:
			print("Unknown person")
	

if __name__ == '__main__':
	# parser = argparse.ArgumentParser()
	# parser.add_argument('input_img', type=str, help='directory of input image')
	# args = parser.parse_args()
	
	known_faces, known_faces_encoding = get_face_list(known_person_dir="./known_person")
	retrive_photos(#args.input_img, 
				   known_faces, 
				   known_faces_encoding, 
				   known_person_dir="./known_person")
