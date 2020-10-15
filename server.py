#import socket module
from socket import *
import threading

serverPort = 12000
allThreads = []

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(1)
print ('Socket prep complete')

class MultiThread(threading.Thread):
    def __init__(self, connectionSocket, ip, port):
        threading.Thread.__init__(self)
        self.connectionSocket = connectionSocket
        self.ip = ip
        self.port = port
        print ('Thread created')

    def run(self):
        while True: 
            try:
                message = connectionSocket.recv(1024).decode()
                print ('Data arrived: ', message)
                if message:
                    filename = message.split()[1]
                    f = open(filename[1:])
                    outputdata = f.read()
                    print(outputdata)
                    #Send one HTTP header line into socket
                    connectionSocket.send("'Keep-Alive':'timeout=5, max=99'\r\n".encode())
                    #Send the content of the requested file to the client
                    for i in range(0, len(outputdata)):
                        connectionSocket.send(outputdata[i])
            except IOError:
                #Send response message for file not found
                connectionSocket.send("404 Not Found\n".encode())                
        #Close client socket
        connectionSocket.close()

while True:
    #Establish the connection
    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print ('TCP connection set up')

    print(addr)

    thread = MultiThread(connectionSocket, addr[0], addr[1])
    thread.start()

    allThreads.append(thread)

    for each in allThreads:
        each.join()

serverSocket.close()
