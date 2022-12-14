import socket
import threading
import random
import json
from multiprocessing import Process

host = '127.0.0.1'                                                

def setupRooms(nrooms):
    rooms = dict()
    ports = random.sample(range(5000, 6000), 3)
    for i in range(nrooms):
        room_name = "Room{}".format(str(i+1))
        room_port = ports[i]
        room_pwd = "{}@123".format(room_name)

        rooms[room_name]= {
            "port": room_port,
            "password": room_pwd
        }

    with open('rooms.json', 'w') as fp:
        json.dump(rooms, fp, indent=4)
    print("{} Rooms created".format(nrooms))
    return ports

def broadcast(message, clients): 
    for client in clients:
        client.send(message)                                        

def handle(client, clients, users):
    while True:
        try:
            message = client.recv(1024)                      
            broadcast(message, clients)                             
        except:
            index = clients.index(client)        
            clients.remove(client)       
            client.close()
            user = users[index]                            
            broadcast('{} left!'.format(user).encode('ascii'), clients)  
            users.remove(user)
            break        
                                       
def receive(port):
    clients = [] 
    users =[]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    server.bind((host, port))                                      
    server.listen(5)                                               
    print("Room Initiliazed... ")

    while True:
        client, address = server.accept()                      
        print("Connected with {}".format(str(address)))    

        client.send('NICK'.encode('ascii'))           
        user = client.recv(1024).decode('ascii')                
        users.append(user)
        clients.append(client)

        print("Name is {}".format(user))

        broadcast("{} joined!".format(user).encode('ascii'), clients)  
        client.send('Connected to server!'.encode('ascii'))       
        thread = threading.Thread(target=handle, args=(client,clients,users,))  
        thread.start()   


if __name__ == '__main__':

    rooms = int(input("Enter the number of rooms you wanted to create: "))
    ports = setupRooms(rooms)

    p1 = Process(target=receive, args=(ports[0],))
    p1.start()
    p2 = Process(target=receive, args=(ports[1],))
    p2.start()
    p3 = Process(target=receive, args=(ports[2],))
    p3.start()

    p1.join()
    p2.join()
    p3.join()

