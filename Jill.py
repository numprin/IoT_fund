#import library that we will use for connection and hashing
import socket
import hashlib

#define Jill class
class Jill_class(object):
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.shared_key = None
    #generate partial key by using Diffie-Hellman Algorithm   
    def generate_partial_key(self):
        partial_key = self.public_key1**self.private_key
        partial_key = partial_key%self.public_key2
        return partial_key
    #generate shared key by using Diffie-Hellman Algorithm
    def generate_shared_key(self, partial_key_r):
        shared_key = partial_key_r**self.private_key
        shared_key = shared_key%self.public_key2
        self.shared_key = shared_key
        return shared_key
    #decrypt message by using Diffie-Hellman Algorithm
    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.shared_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c)-key)
        return decrypted_message

# define HOST and PORT that We want to have connection 
# HOST is IP of the server
HOST = 'localhost'
PORT = 5000
 
 # define Jill's public and private key and Jack's public key
Jack_public = 523
Jill_public = 511
Jill_private = 567

#construct object from class
Jill = Jill_class(Jack_public,Jill_public,Jill_private)
#generate partial key from method
partial_key = Jill.generate_partial_key()
#generate shared key from method
shared_key = Jill.generate_shared_key(partial_key)
#constuct Socket's object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Jill behave like Server so We will bind object to Host and port
s.bind((HOST,PORT))
#Jill have to wait for Jack's connection
s.listen()

while True:
    print("Waiting for Jack's message")
    # accept connection from Jack
    connection, client_address = s.accept()
    try:
        print("Jack has connected")
        while True:
            #define data's size to receive from Jack
            data = connection.recv(1024)
            print("received message is ", data.decode())
            break 
    finally:
        #After receiveing data We have to close connection
        connection.close()
        print("Closed connection")
        break
#Decrypt message from Jack
decrypted_message = Jill.decrypt_message(data.decode())
print("decrypted_message is ",decrypted_message)

#Jill use hash function to generate a cipher text of Hello world
Jill_hash = hashlib.sha384(b"Hello world!")
#write hashed message down to passphase.txt
write_text = open('passphase.txt','w')
write_text.write(Jill_hash.hexdigest())
write_text.close()

#hash decrypted message
Jill_hash_received = hashlib.sha384(decrypted_message.encode())
Jill_hash_received = Jill_hash_received.hexdigest()

#read passphase.txt
read_text = open('passphase.txt','r')
text_from_passphase = read_text.read()
read_text.close()
#print text from passphase.txt and message digest
print("text_from_passphase.txt is ",text_from_passphase )
print("Hashed encrypted message is ",Jill_hash_received)

#print whether both of them are identical or not
if text_from_passphase == Jill_hash_received:
    print("Text from passphase.txt and Hashed text from decrypted message are identical")
else:
    print("Text from passphase.txt and Hashed text from decrypted message are not identical")