from re import T
import string
from cv2 import split
import face_recognition
import cv2
import numpy as np
import os
import glob

faces_encodings = []
faces_names = []
cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'data/Zdjecia/')
list_of_files = [f for f in glob.glob('Zdjecia/'+'*.jpg')]
number_files = len(list_of_files)
names = list_of_files.copy()

def trainImages():
    for i in range(number_files):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        faces_encodings.append(globals()['image_encoding_{}'.format(i)])
        # Create array of known names
        names[i] = names[i].replace(cur_direc, "")  
        faces_names.append(names[i])

def recognizeFace(frame):
    trainImages()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations( rgb_small_frame)
    face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
    face_names = []
    rozpoznano = False
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces (faces_encodings, face_encoding)
        name = "Nieznany"
        face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = faces_names[best_match_index]
            rozpoznano = True
        
        face_names.append(name)

            # process_this_frame = not process_this_frame
            
            # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
                # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            if rozpoznano:
                text = name.split("\\")
                text = text[1].split(".")
                name = text[0]
            
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # Display the resulting image
            # cv2.imshow('Video', frame)
            return frame
