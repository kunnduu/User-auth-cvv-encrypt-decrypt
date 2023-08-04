# User-auth-cvv-encrypt-decrypt
This project is used to replace the OTP verification method with face recognition to verify the user accounts and uses different algorithm to encrypt and decrypt the sensitive details like  cvv using a random algo out of the four everytime
The user initiates a connection to the server through socket programming.
● The server generates a secret key and shares it with the user over the socket 
connection.
● Once the key is received, the user can access the GUI.
● The GUI initiates face detection to authenticate the user by asking the account 
number .
● If the user is successfully authenticated, the GUI prompts the user to enter their 
details. Otherwise if someone else is trying to access your account the program 
stops executing
● The user enters their details, and the data is secured using a random algorithm out 
of TDES, CAST, Blowfish, and AES.
● The encrypted data is sent to the server .
● The server decrypts the data using the same algorithm used for encryption 
