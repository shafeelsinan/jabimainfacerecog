# import the opencv library
import face_recognition
import cv2
import numpy as np
import csv
import os
import glob
from datetime import datetime
  
  
# define a video capture object
video_capture = cv2.VideoCapture(0)

#jobs_image = face_recognition.load_image_file("photos/jobs.jpeg")
#jobs_encoding = face_recognition.face_encodings(jobs_image)[0]

#ratan_image = face_recognition.load_image_file("photos/ratan.jpeg")
#ratan_encoding = face_recognition.face_encodings(ratan_image)[0]

#sinan_image = face_recognition.load_image_file("photos/sinan.jpeg")
#sinan_encoding = face_recognition.face_encodings(sinan_image)[0]

images_path = glob.glob(os.path.join("photos/", "*.*"))

print("{} encoding images found.".format(len(images_path)))
known_face_encoding = []
known_face_names = []

for img_path in images_path:
    img = cv2.imread(img_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Get the filename only from the initial file path.
    basename = os.path.basename(img_path)
    (filename, ext) = os.path.splitext(basename)
    # Get encoding
    img_encoding = face_recognition.face_encodings(rgb_img)[0]

    # Store file name and file encoding
    known_face_encoding.append(img_encoding)
    known_face_names.append(filename)
print("Encoding images loaded")

#known_face_encoding = [
#jobs_encoding,
#ratan_encoding,
#sinan_encoding]

#known_face_names = [
#"jobs",
#"ratan",
#"sinan"]

students = known_face_names.copy()

face_locations = []
face_encodings = []
face_names =[]
s = True
detected = False
detectedname=""

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")


f = open(current_date+'.csv','w+',newline='')
lnwriter = csv.writer(f)

while True:
    _,frame = video_capture.read()
    small_frame =  cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    #rgb_small_frame = small_frame[:,:,::-1]
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name= known_face_names[best_match_index]  
            face_names.append(name)
            if name in known_face_names:
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])
                    #print(name+"Detected")
                    detected = True
                    detectedname = name
    cv2.imshow("Attendance System",frame)
    if(detected):
        print(detectedname+"Detected")
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
f.close()
