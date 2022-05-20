# import socket library that we will use for send and receive message between computer
import socket
# define Jack's class
class Jack_class(object):
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
    #generate Shared key by using Diffie-Hellman Algorithm
    def generate_shared_key(self, partial_key_r):
        shared_key = partial_key_r**self.private_key
        shared_key = shared_key%self.public_key2
        self.shared_key = shared_key
        return shared_key
    #Encrypt message by using Diffie-Hellman Algorithm
    def encrypt_message(self, message):
        encrypted_message = ""
        key = self.shared_key
        for c in message:
            encrypted_message += chr(ord(c)+key)
        return encrypted_message
    
# define HOST and PORT that We want to have connection 
# HOST is IP of the server
HOST = 'localhost'
PORT = 5000

# define Jack's public and private key and Jill's public key
Jack_public = 523
Jack_private = 123
Jill_public = 511

# define message that we want to send to Jill
message = "Hello world!"

# construct object from class
Jack = Jack_class(Jack_public,Jill_public,Jack_private)

# generate partial key that we will use this key to generate shared key
partial_key = Jack.generate_partial_key()

#genereate Shared key from partial key
shared_key = Jack.generate_shared_key(partial_key)

#Encrypt the message by using method from class
encrypted_message = Jack.encrypt_message(message)

#Construct Socket object
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Connect to Jill just like client connect to server
s.connect((HOST,PORT))
#Send the encypted message to Jill
s.sendall(encrypted_message.encode())
#Close connection
s.close()