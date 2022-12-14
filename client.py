import socket
import sys
import threading
import json

with open('rooms.json', 'r', encoding='utf-8') as fp:
    rooms = json.load(fp)

print("Available Rooms:")
for room in rooms:
    print(room, end = "\n")


room_name = input("Enter the room you wanted to enter: ")

validflag = False
for _ in range(3):
    room_pwd = input("Enter the password for {}: ".format(room_name))
    if room_pwd == rooms[room_name]["password"]:
        print("\nEntering {}...\n".format(room_name))
        validflag = True
        break
    else:
        print("Access Denied! Try again.")

if not validflag:
    print("Try again with valid password")
    exit()

user = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', int(rooms[room_name]["port"])))               

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')  
            if message == "NICK":
                client.send(user.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:  
        message = '{}: {}'.format(user, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start() 