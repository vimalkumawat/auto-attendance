import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import keyboard


path = "img"                      #images File folder
images = []
classname =[]
mylist = os.listdir(path)
#print(mylist)

for cl in mylist:
    cr_img = cv2.imread(f'{path}/{cl}')
    images.append(cr_img)
    classname.append(os.path.splitext(cl)[0])

def markattendance(name):                          #For attendance entry
    with open('Attendance.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                  entry = line.split(',')
                  nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')


#print(classname)

def find_encodings(images):
    encode =[]
    for imgg in images:
        imgg = cv2.cvtColor(imgg, cv2.COLOR_BGR2RGB)
        encod = face_recognition.face_encodings(imgg)[0]
        encode.append(encod)
    return encode

encod_list = find_encodings(images)
print("encoding camplete")
cap = cv2.VideoCapture(0)
while True:
    succsess,img= cap.read()
    #img = cv2.resize(img,(0,0),None,.5,.5)
    cap.set(10, 1000)  # id 10 for brightness w
    imgC = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    locCurFrame = face_recognition.face_locations(imgC)
    encodCurFrame = face_recognition.face_encodings(imgC,locCurFrame)

    for encodF,locF in zip(encodCurFrame,locCurFrame):
        matches = face_recognition.compare_faces(encod_list,encodF)
        dis = face_recognition.face_distance(encod_list,encodF)
        #print(dis)
        matchindex = np.argmin(dis)

        if matches[matchindex]:
            name = classname[matchindex].upper()
            #print(name)
            y1,x2,y2,x1 =locF
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),thickness=2)
            cv2.rectangle(img,(x1,y2-5),(x2,y2+10),(0,0,255),cv2.FILLED)
            cv2.putText(img,name, (x1+4, y2+ 6), cv2.FONT_HERSHEY_COMPLEX, .5,
                        (255, 255, 255))
            markattendance(name)
    if keyboard.is_pressed('q'):                                     # if key 'q' is pressed
        print('You Pressed A Key!')
        break                                                       # finishing the loopq

    cv2.imshow("webcame",img)
    cv2.waitKey(1)


"""FOR SENDING Gmail"""



import smtplib
import mimetypes
from email.message import EmailMessage
message = EmailMessage()
sender = "<sender@gmail.com>"                                                 #sender email id
recipient = "<reciver@gmail.com>"
message['From'] = sender
message['To'] = recipient
message['Subject'] = 'Attendene'
body = """Attendene """
message.set_content(body)
mime_type, _ = mimetypes.guess_type('Attendance.csv')        #sending file name
mime_type, mime_subtype = mime_type.split('/')
with open('Attendance.csv', 'rb') as file:                    #sending file name
 message.add_attachment(file.read(),
 maintype=mime_type,
 subtype=mime_subtype,
 filename='Attendance.csv')                                     #sending file name
print(message)
mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
mail_server.set_debuglevel(1)
mail_server.login(sender, '<Sender email password')                       #sender email password
mail_server.send_message(message)
mail_server.quit()


