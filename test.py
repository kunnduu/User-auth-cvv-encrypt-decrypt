import cv2
import sys
sys.path.append("C:\\Users\\kundu\\PycharmProjects\\Auth\\venv\\Lib\\site-packages")
import numpy as np
import face_recognition
import os
import tkinter as tk
import datetime
import time
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.Cipher import CAST
from os import urandom
import blowfish
from base64 import b64encode
from base64 import b64decode
from Crypto import Random
from Crypto.Util.Padding import pad
#from binascii import a2b_hex
import csv
# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server and decoding to get the string.

# close the connection
#s.close()


path = 'images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)


# Function to calculate encodings
def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Covert to RGB
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList




#Assigning Algorithms Numbers :-
#0 -> RSA
#1 -> AES
#2 -> TDES
#3 -> BLOWFISH
#4 -> CAST


def BlowfishEncrypt(key,cvv,cardno):
    cipher = blowfish.Cipher(key)
    iv = urandom(8) # initialization vector

    data = cvv + cardno
    #data=input('Enter the Data to encrypt:')
    while((len(data)%8)!=0):
        data=data+" "
    res = data.encode('utf-8')
    print("Data to encrypt",data)
    ciphertext = b"".join(cipher.encrypt_cbc(res, iv))
    print("encrypted data",ciphertext)
    s.send(ciphertext)
    cipher = [b64encode(ciphertext).decode('utf-8'),b64encode(iv).decode('utf-8')]
    s.close()

    with open('ciphertext.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the data(cipher,iv)
        writer.writerow(cipher)

        f.close()

def CASTEncrypt(key,cvv,cardno):
    cipher = CAST.new(key, CAST.MODE_OPENPGP)

    plaintext = cvv+cardno
    plaintext = plaintext.encode()
    msg = cipher.encrypt(plaintext)
    eiv = msg[:CAST.block_size+2]
    ciphertext = msg[CAST.block_size+2:]
    print("The encrypted data is:", b64encode(ciphertext).decode('utf-8'))
    print("The iv is:", b64encode(eiv).decode('utf-8'))
    cipher = [b64encode(ciphertext).decode('utf-8'), b64encode(eiv).decode('utf-8')]
    s.send((b64encode(eiv).decode('utf-8')).encode())
    s.close()

    with open('ciphertext.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the data(cipher,iv)
        writer.writerow(cipher)

        f.close()
def AESEncrypt(key,cvv,cardno):

    plain_text = cvv+cardno
    plain_text = plain_text.encode()
    # Generate a non-repeatable key vector with a length
    # equal to the size of the AES block
    iv = Random.new().read(AES.block_size)
    # Use key and iv to initialize AES object, use MODE_CBC mode
    mycipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = mycipher.encrypt(pad(plain_text,AES.block_size))
    print("The encrypted data is:", b64encode(ciphertext).decode('utf-8'))
    print("The iv is:", b64encode(iv).decode('utf-8'))
    cipher = [b64encode(ciphertext).decode('utf-8'),b64encode(iv).decode('utf-8')]
    s.send((b64encode(iv).decode('utf-8')).encode())
    s.close()

    with open('ciphertext.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the data(cipher,iv)
        writer.writerow(cipher)

        f.close()


def tripledesencrypt(bkey,cvv,cardno):

    msg=cvv+cardno
    key = pad(bkey,24)
    tdes_key = DES3.adjust_key_parity(key)
    cipher = DES3.new(tdes_key,DES3.MODE_EAX, nonce=b'0')
    ciphertext = cipher.encrypt(msg.encode('utf-8'))
    print("Encrypted text :-", ciphertext)
    s.send(ciphertext)
    cipher = [b64encode(ciphertext).decode('utf-8')]
    s.close()
    with open('ciphertext.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(cipher)
        f.close()

def compute(a,m,n):
    y=1
    while(m>0):
        r=m%2
        if(r==1):
            y=(y*a)%n
        a = a*a % n
        m = m // 2
    return y


encodeListKnown = findEncoding(images)
print('Encoding complete')
# Initializing web cam to match image

def vid_capture(): #face capture function
    cap = cv2.VideoCapture(0)
    acc = (txt.get())
    x = 1
    while (x == 1):
        success, img = cap.read()
        imgSmall = cv2.resize(img, (0, 0), None, 0.25,
                              0.25)  # Reduciing the size to 1/4 th as we are doing it in real time makes it faster process
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)  # Covert to RGB
        # A frame can have multiple faces
        facesCurrFrame = face_recognition.face_locations(imgSmall)
        encodeCurr = face_recognition.face_encodings(imgSmall, facesCurrFrame)
        # Looping through the current faces in list and then matching it with all the images in folder
        for encodFace, faceLoc in zip(encodeCurr, facesCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodFace)
            print(matches)
            faceDis = face_recognition.face_distance(encodeListKnown,
                                                     encodFace)  # Will give us three values as 3 images the lowest distance will be the best match
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex]
                if (name == acc):
                    print('Account found')
                    x = 0
                    break
                else:
                    print('Account not found maybe wrong account number or someone else trying to access the account')
                    exit(0)
            else:
                print('No account found')
                exit(0)

def send_data(): #send key to receiver
    cvv = (txt2.get())
    print(cvv)
    cardno = (txt3.get())
    keyrecieved = s.recv(1024).decode()
    print("The recived key is ", keyrecieved)
    print("Algo Number : ", keyrecieved[0])
    with open("C:\\Users\\kundu\\PycharmProjects\\Auth\\key.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if (len(row) == 0):
                break
            keyrecieved = row[0]
        csv_file.close()

    # keyrecieved = input("Enter the key recieved by the reciever side : ")

    algonumber = keyrecieved[0]
    key = keyrecieved[1:]
    print(algonumber)
    print(key)
    if (algonumber == '1'):
        key = b64decode(key)
        print("KEY :", key)
        AESEncrypt(key,cvv,cardno)

    elif (algonumber == '2'):
        key = b64decode(key)
        print("KEY :", key)
        tripledesencrypt(key,cvv,cardno)
    elif (algonumber == '4'):
        key = b64decode(key)
        print("KEY :", key)
        CASTEncrypt(key,cvv,cardno)

    elif (algonumber == '3'):
        key = b64decode(key)
        print("KEY :", key)
        BlowfishEncrypt(key,cvv,cardno)


##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


###################################################################################

'''keyrecieved=s.recv(1024).decode()
print("The recived key is ",keyrecieved)
print("Algo Number : ",keyrecieved[0])'''
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x600")
window.resizable(True, True)
window.title("ABC Bank")
window.configure(background='#262523')

frame2 = tk.Frame(window, bg="#00aeff")
frame2.place(relx=0.25, rely=0.17, relwidth=0.48, relheight=0.80)

message3 = tk.Label(window, text="ABC Bank Login", fg="white", bg="#262523", width=55,
                    height=1, font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |  ", fg="orange", bg="#262523", width=55,height=1, font=('times', 22, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="orange", bg="#262523", width=55, height=1, font=('times', 22, ' bold '))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="                          Login credentials + Encryption                          ", fg="black",
                 bg="#3ece48", font=('times', 17, ' bold '))
head2.grid(row=0, column=0)

lbl = tk.Label(frame2, text="Enter Account number", width=20, height=1, fg="black", bg="#00aeff", font=('times', 17, ' bold '))
lbl.place(x=175, y=55)

txt = tk.Entry(frame2, width=32, fg="black", font=('times', 15, ' bold '))
txt.place(x=150, y=88)

lbl2 = tk.Label(frame2, text="Enter CVV", width=20, fg="black", bg="#00aeff", font=('times', 17, ' bold '))
lbl2.place(x=182, y=180)

txt2 = tk.Entry(frame2, width=32, fg="black", font=('times', 15, ' bold '))
txt2.place(x=150, y=213)

lbl3 = tk.Label(frame2, text="Enter Card Number", width=20, fg="black", bg="#00aeff", font=('times', 17, ' bold '))
lbl3.place(x=182, y=250)

txt3 = tk.Entry(frame2, width=32, fg="black", font=('times', 15, ' bold '))
txt3.place(x=150, y=293)

message = tk.Label(frame2, text="", bg="#00aeff", fg="black", width=39, height=1, activebackground="yellow",
                   font=('times', 16, ' bold '))
message.place(x=7, y=450)

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('times', 29, ' bold '), menu=filemenu)

###################### BUTTONS ##################################

auth = tk.Button(frame2, text="Authenticate", command=vid_capture, fg="black", bg="yellow", width=11,
                         activebackground="white", font=('times', 11, ' bold '))
auth.place(x=267, y=140)

send = tk.Button(frame2, text="Verify", command=send_data, fg="black", bg="yellow", width=11,
                         activebackground="white", font=('times', 11, ' bold '))
send.place(x=267, y=330)

window.configure(menu=menubar)
window.mainloop()



#################################################################################









cv2.waitKey(1)