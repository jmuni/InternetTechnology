# python as.py asListenPort ts1Hostname ts1ListenPort_a ts2Hostname ts2ListenPort_a

import threading
import time
import random
import socket
import sys


# Lists to store everything
hostList = ["x"]
hostLowerList = ["x"]
ipList = ["x"]
flagList = ["x"]

ts_com = ""
ts_edu = ""

# Make sure port entered is valid
def checkPort(portNum):
    try:
        portNum = int(portNum)
        if int(portNum) < 1 or int(portNum) > 65535:
            raise ValueError
        else:
            return portNum
    except ValueError:
        print("Invalid Port number, enter a number between 1 and 65535")
        exit()

# Start the server and make connections 
def startServer(port):
    portNumber = int(port)
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[AS]: Server socket created")
    except socket.error as err:
        print('AS socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', portNumber)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[AS]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[AS]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[AS]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.  
    msg = "Client to AS Connection Successful!"
    csockid.send(msg.encode('utf-8'))
    
      
    ts1 = connectTS1(ts1Host, ts1Port_a)
    ts2 = connectTS2(ts2Host, ts2Port_a)
    ts1success = ts1.recv(200)
    print("[AS]: Success message here TS1=={}".format(ts1success)) 
    ts2success = ts2.recv(200)
    print("[AS]: Success message here TS2=={}".format(ts2success))
    
    csockid.send(ts1Host.encode('utf-8'))
    h1success = csockid.recv(200)
    csockid.send(ts2Host.encode('utf-8'))
    h1success = csockid.recv(200)

    print("TS1 Hostname: " + ts1Host)
    print("TS2 Hostname: " + ts2Host)

    # Keep the program running
    while(1):
       cChallenge, cDigest = fromClient(csockid, ts1, ts2)
       #print("[AS]: cChallenge is {}".format(cChallenge))
       #print("[AS]: cDigest is {}".format(cDigest))
       #print("[AS]: Challenge and Digest returned")
       #send Digest to T1 and T2, recieve 
       ts1.send(cChallenge.encode('utf-8'))
       print("[AS]: Challenge sent to ts1: {}".format(cChallenge))
       digest1 = ts1.recv(200) 
       print("[AS]: Digest 1 is {}".format(digest1))        
       
       ts2.send(cChallenge.encode('utf-8'))
       print("[AS]: Challenge sent to ts2: {}".format(cChallenge))
       digest2 = ts2.recv(200)
       print("[AS]: Digest 2 is {}".format(digest1)) 
       
       #if cdigest matches digest1, AS sends HOSTNAME of TS1
       #if it matches digest2, AS sends HOSTNAME of TS2 
       #and worse case no match, sends NO HOST FOUND
       if cDigest == digest1:
          #ints1 = "ts1"
          #csockid.send(ints1.encode('utf-8')
          host1 = "ts1"
          csockid.send(host1.encode('utf-8')) 
          print("[AS]: ts1 sent to client")
       elif cDigest == digest2:
          host2 = "ts2"
          csockid.send(host2.encode('utf-8'))
          print("[AS]: ts2 sent to client")
       else:
          nohost = "NO HOST FOUND"
          csockid.send(nohost.encode('utf-8'))
          print("[AS]: NOHOST sent to client")   
         
    #thats ALL AS does... 

    
    # Close the server socket
    ss.close()
    exit()


def connectTS1(hostName, port):
    
    portNumber = int(port)

    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[AS]: TS1 socket created")
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
        print("[AS]: TS2 socket created")
    except socket.error as err:
        print('TS2 socket open error: {} \n'.format(err))
        exit()

    host_addr = socket.gethostbyname(hostName)

    # connect to the server on given host and port number
    server_binding = (host_addr, portNumber)
    ts2.connect(server_binding)
    return ts2 

# Receive and send data from and to client
def fromClient(csockid, ts1, ts2):
    # Receive data from the client
    data_from_client=csockid.recv(200)
    print("[AS]: [C] sent {}".format(data_from_client))
    if(data_from_client=="END"):
        print("Client closed, shutting down...")
        ts1.send("END")
        ts2.send("END")
        exit()
    temp = data_from_client.split()
    
    #AS recieves challenge and digest from Client
    challenge = temp[0]
    digest = temp[1]
    print("[AS]: Challenge recv: {}".format(challenge))
    print("[AS]: Digest recv: {}".format(digest))
    
    #AS sends ONLY challenge to TS1 AND TS2, recieves 2 digests, then compares digests to client digest
    return challenge, digest



if __name__ == "__main__":
    if (len(sys.argv) > 6):
        print("Too many arguments. Check Syntax")
        print("python as.py asListenPort ts1Hostname ts1ListenPort_a ts2Hostname ts2ListenPort_a")
        exit()
    if (len(sys.argv) < 6):
        print("Too few arguments. Check Syntax")
        print("python as.py asListenPort ts1Hostname ts1ListenPort_a ts2Hostname ts2ListenPort_a")
        exit()
		
    asPort = sys.argv[1]
    ts1Host, ts1Port_a = sys.argv[2], sys.argv[3] 
    ts2Host, ts2Port_a = sys.argv[4], sys.argv[5] 
    checkPort(asPort)    
    # all socket and networking things
    # parameters -- rsPortNumber
    startServer(asPort)
    #connectTS1(ts1Host, ts1Port_a)
    #connectTS2(ts2Host, ts2Port_a)
    