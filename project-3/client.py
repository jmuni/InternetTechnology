# python client.py asHostname asListenPort ts1ListenPort_c ts2ListenPort_c


import threading
import time
import random

import socket
import sys
import hmac

# List for everything that is going to be in the final RESOLVED.txt
finalList = []

# Connecting the AS server
def connectAS(hostName, port):
    portNumber = int(port)  

    try:
        auth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('AS socket open error: {} \n'.format(err))
        exit()

    host_addr = socket.gethostbyname(hostName)

    # connect to the server on given host and port number
    server_binding = (host_addr, portNumber)
    auth.connect(server_binding)

    # getting data from server
    data_from_server=auth.recv(200)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))
    
    host1 = auth.recv(200)
    print("[C]: AS SENT TS1 HOST: {}".format(host1))
    success1 = "host1 recvd"
    auth.send(success1.encode('utf-8'))
    
    host2 = auth.recv(200)
    print("[C]: AS SENT TS2 HOST: {}".format(host2))
    auth.send(success1.encode('utf-8'))
    
    print ("[C]: Attempt TS1 Connection")
    ts1 = connectTS1(host1, ts1Port)
    ts1success = ts1.recv(200)
    print("[C]: TS1 Connection Success =={}".format(ts1success))
    
    print ("[C]: Attempt TS2 Connection")
    ts2 = connectTS2(host2, ts2Port)
    ts2success = ts2.recv(200)
    print("[C]: TS2 Connection Success =={}".format(ts2success))
    

    # Client goes through the list to send messages to RS
    sendAS(auth, ts1, ts2)
    auth.send("END")
    ts1.send("END")
    ts2.send("END")

    # Close connection
    auth.close()
    
def connectTS1(hostName, port):
    
    portNumber = int(port)

    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: TS1 socket created")
    except socket.error as err:
        print('TS1 socket open error: {} \n'.format(err))
        exit()

    host_addr = socket.gethostbyname(hostName)

    # connect to the server on given host and port number
    server_binding = (host_addr, portNumber)
    ts1.connect(server_binding)
    return ts1
    

    
def connectTS2(hostName, port):
    
    portNumber = int(port)

    try:
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: TS2 socket created")
    except socket.error as err:
        print('TS2 socket open error: {} \n'.format(err))
        exit()

    host_addr = socket.gethostbyname(hostName)

    # connect to the server on given host and port number
    server_binding = (host_addr, portNumber)
    ts2.connect(server_binding)
    return ts2

def sendAS(auth, ts1, ts2):
   # Open file and read one line at a time
   f = open("PROJ3-HNS.txt", "r")
   print("Opening file: " + f.name)
   print("\n")
   f1 = f.readlines()


    # Send hostnames to RS or TS servers as needed
   ts1connection = 0
   ts2connection = 0
   
   for lines in f1:
        lines = lines.rstrip("\n")
        # Send line to RS to check first
  
        #this part is for part3. Client reads each line, generates digest and sends that to AS instead
        #do I need to check for lower/upper case?? ===
        temp = lines.split()
        key, challenge, query = temp[0], temp[1], temp[2]  
  
  	digest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8"))
	print ("[C]: Digest was made: {}".format(digest.hexdigest()))
	newDigest = digest.hexdigest()
	sendAS = challenge + " " + str(newDigest)
	print ("[C]: Client sends to AS: {}".format(sendAS))
  
        auth.send(sendAS.encode('utf-8'))
        print("-----------------------")
        print("Digest Sent!")
        
        #after digest is sent, AS sends ONE HOSTNAME (ex ts1.edu) and then Client CONNECTS with that TS
        #client sends query (ex www.princeton.edu)
        
        authHost = asInfo(auth)
        print("[C]: AS reads Digest and returns hostname: {}".format(authHost))
        if "ts1" in authHost:
           #we get the ts1 hostname for the firsttime and attempt to connect
           #if ts1connection == 0:
              #print ("[C]: First time TS1 Connection")
              #connectTS1(asHost, ts1Port)
              #ts1success = ts1.recv(200)
              #print("[C]: TS2 Connection Success =={}".format(ts1success))
              #ts1connection = 1 
           #sends query to TS1 if found, it returns all that good stuff
           print("QUERY: {}".format(query))
           ts1.send(query)
           #recieves message from 
           recvMessage(ts1)
        elif "ts2" in authHost:
           #we get the ts2 hostname for the firsttime and attempt to connect
           #if ts2connection == 0:
              #print ("[C]: First time TS2 Connection")
              #connectTS2(asHost, ts2Port)
              #ts2success = ts2.recv(200)
              #print("[C]: TS2 Connection Success =={}".format(ts2success))
              #ts2connection = 1 
           #sends query to TS1 if found, it returns all that good stuff
           print("QUERY: {}".format(query))
           ts2.send(query)
           #recieves message from 
           recvMessage(ts2)  
        else:
           print("[C]: asHost was NOT FOUND: {}".format(asHost))   
           
        
        #recvMessage(rs)

#recieved message from AS
def asInfo(auth):
   data = auth.recv(200)
   temp = data.decode('utf-8')
   temp = temp.strip()
   
   print("[C] recieved from [AS]: {}".format(temp))
   return temp
   

# Getting messages from RS server only.
def recvMessage(temp):
    data = temp.recv(200)
    temp = data.decode('utf-8')

    print("Found!: " + temp.strip())
    finalList.append(temp + "\n")
    print(temp)

if __name__ == "__main__":
    if (len(sys.argv) > 5):
        print("Too many arguments. Check Syntax")
        print("python client.py asHostname asListenPort ts1ListenPort_c ts2ListenPort_c")
        exit()
    if (len(sys.argv) < 5):
        print("Too few arguments. Check Syntax")
        print("python client.py asHostname asListenPort ts1ListenPort_c ts2ListenPort_c")
        exit()
	
    # all socket and networking things
    # parameters -- rsHostname and rsPortNumber
    asHost, asPort = sys.argv[1], sys.argv[2]
    ts1Port, ts2Port = sys.argv[3], sys.argv[4]
    connectAS(asHost, asPort)

    print("-------------------------------------")
    # Final Answer
    print("Here is the final answer (Also, in RESOLVED.txt file)")
    for x in finalList:
        print(x)
    print("-------------------------------------")

    listLen = len(finalList)
    
    f = open("RESOLVED.txt", "w+")
    for i in range(listLen):
        f.write(finalList[i])


    print("Done.")
