# User-auth-cvv-encrypt-decrypt
This project is used to replace the OTP verification method with face recognition to verify the user accounts and uses different algorithm to encrypt and decrypt the sensitive details like  cvv using a random algo out of the four every time.
The user initiates a connection to the server through socket programming.

1) The server generates a secret key and shares it with the user over the socket 
connection.
2) Once the key is received, the user can access the GUI.
3) The GUI initiates face detection to authenticate the user by asking for the account 
number.
4) If the user is successfully authenticated, the GUI prompts the user to enter their 
details. Otherwise, if someone else is trying to access your account the program 
stops executing
5) The user enters their details, and the data is secured using a random algorithm out 
of TDES, CAST, Blowfish, and AES.
6) The encrypted data is sent to the server.
7) The server decrypts the data using the same algorithm used for encryption 

Requirements: dlib library , crypto library , cv2
