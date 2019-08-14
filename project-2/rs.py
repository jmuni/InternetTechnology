# python rs.py rsListenPort tsEduListenPort tsComListenPort

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

# Start the server and make connections 
def startServer(port):
    portNumber = int(port)
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', portNumber)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.  
    msg = "Connection Successful!"
    csockid.send(msg.encode('utf-8'))
    # Open file and store all the host names and ip and flags
    openFile()
    findServerNames()
    edu, com = startNextSevers()
    print("ts_com: " + ts_com)
    print("ts_edu: " + ts_edu)

    # Keep the program running
    while(1):
        recvMessage(csockid, edu, com)

    # Close the server socket
    ss.close()
    exit()

def startNextSevers():
    # global ts_com
    # global ts_edu
    print("Do something here soon")
    print("Connect to this server: " + ts_com)
    print("Conect to this server: " + ts_edu)

    indexEDU = hostLowerList.index(ts_edu)
    print(indexEDU)
    print("EDU SERVER: " + hostLowerList[indexEDU] + " " + ipList[indexEDU] + " " + sys.argv[2])

    indexCOM = hostLowerList.index(ts_com)
    print(indexCOM)
    print("COM SERVER: " + hostLowerList[indexCOM] + " " + ipList[indexCOM] + " " + sys.argv[3])

    portEDU = int(sys.argv[2])
    portCOM = int(sys.argv[3])

    print("Connecting to " + ts_edu)
    try:
        edu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    host_addr = socket.gethostbyname(ipList[indexEDU])

    server_binding = (host_addr, portEDU)
    edu.connect(server_binding)

    # data = edu.recv(200)
    # print("[C]: Data received from EDU server: {}".format(data.decode('utf-8')))

    # edu.send("Success!")
     
     # -----------------------------------------------------------
    
    print("Connecting to " + ts_com)

    try:
        com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    host_addr = socket.gethostbyname(ipList[indexCOM])

    server_binding = (host_addr, portCOM)
    com.connect(server_binding)

    # data = com.recv(200)
    # print("[C]: Data received from COM server: {}".format(data.decode('utf-8')))

    # com.send("Success!")

    # # Close connection
    # edu.close()
    # com.close()
    return edu, com

# Open file and store in lists
def openFile():
    print("---------File Things-------")
    f = open("PROJ2-DNSRS.txt", "r")
    print (f.name)
    f1 = f.readlines()
    for x in f1:
        print(x)
        host, ip, flag = x.split(' ', 3)
        hostList.append(host)
        hostLowerList.append(host.lower())
        ipList.append(ip)
        flagList.append(flag.strip())

    f.close()

# Find the new servers and store them into ts_com and ts_edu.
# Use this later to find index and then use it to find the IP address.
def findServerNames():
    global ts_com
    global ts_edu
    listLen = len(flagList)
    for i in range(listLen):
        if(flagList[i] == "NS"):
            serverName = hostLowerList[i]
            nameLen = len(serverName)
            print(nameLen)
            print(serverName)
            if(serverName[nameLen-4] == '.' and serverName[nameLen-3] == 'c' and serverName[nameLen-2] == 'o' and serverName[nameLen-1] == 'm'):
                print("COM: " + serverName)
                ts_com = serverName
            if(serverName[nameLen-4] == '.' and serverName[nameLen-3] == 'e' and serverName[nameLen-2] == 'd' and serverName[nameLen-1] == 'u'):
                print("EDU: " + serverName)
                ts_edu = serverName


# Receive and send data from and to client
def recvMessage(csockid, edu, com):
    # Receive data from the client
    data_from_client=csockid.recv(200)
    strHost = data_from_client.strip()

    if (strHost != ""):
        print("[S]: Client: |{}|".format(strHost))
        temp = strHost.lower()
        val = findName(temp)
        tempLen = len(temp)
        if val != -1:
            host = hostList[val]
            ip = ipList[val]
            flag = flagList[val]
            finalStr = host + " " + ip + " " + flag
            print(finalStr)
            csockid.send(finalStr)
        elif val == -1:
            # Need to switch back to other list to make sure it is in the same case
            print("NOT FOUND IN RS, sending to TS_COM OR TS_EDU!")
            if(temp[tempLen-4] == '.' and temp[tempLen-3] == 'c' and temp[tempLen-2] == 'o' and temp[tempLen-1] == 'm'):
                print("COM: |{}|".format(temp))
                com.send(temp)
                newData = com.recv(200)
                print("NEWDATA: |{}|".format(newData))
                csockid.send(newData)
            elif(temp[tempLen-4] == '.' and temp[tempLen-3] == 'e' and temp[tempLen-2] == 'd' and temp[tempLen-1] == 'u'):
                print("EDU: |{}|".format(temp))
                edu.send(temp)
                newData = edu.recv(200)
                print("NEWDATA: |{}|".format(newData))
                csockid.send(newData)
            else:
                finalStr = temp + " - Error:HOST NOT FOUND"
                print(finalStr)
                csockid.send(finalStr)

    return

# Find the hostname in the list
def findName(strHost):
    print("------------------")
    print(strHost)
    val = -1
    if strHost in hostLowerList:
        val = hostLowerList.index(strHost)
        print("Found!")
    print("------------------")
    return val


if __name__ == "__main__":

    # all socket and networking things
    # parameters -- rsPortNumber
    startServer(sys.argv[1])

