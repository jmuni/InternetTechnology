import threading
import time
import random
import socket
import sys
import hmac
import select

# python ts1.py ts1ListenPort_a ts1ListenPort_c
# ts1ListenPort_a ---> Used to connect with AS
# ts1ListenPort_c ---> Used to connect with CLIENT

# Lists to store everything
hostList = ["x"]
hostLowerList = ["x"]
ipList = ["x"]
flagList = ["x"]


def getKey():
    print("---------File Things-------")
    f = open("PROJ3-KEY1.txt", "r")
    print (f.name)
    f1 = f.readlines()
    for x in f1:
        print(x)
        key = x.strip()
    f.close()
    print(key)
    return key


def connectAS():
    portNumber = int(sys.argv[1])
    print(portNumber)
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
    auth, addr = ss.accept()
    print ("[S]: Got a connection request from a AS at {}".format(addr))

    #send a message to client
    msg = "AS to TS1 Connection Successful!"
    auth.send(msg.encode('utf-8'))
    return auth


def connectClient():
    portNumber = int(sys.argv[2])
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
    client, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    #send a message to client
    msg = "Client to TS1 Connection Successful!"
    client.send(msg.encode('utf-8'))
    return client

def openFile():
    print("---------File Things-------")
    f = open("PROJ3-DNSTS1.txt", "r")
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

def sendReceive(auth, client, key_query):
    challenge = auth.recv(200)
    if(challenge=="END"):
        print("Client closed, shutting down...")
        exit()
    print("|{}|".format(challenge))

    # Create digest
    digest = hmac.new(key_query.encode("utf-8"), challenge.encode("utf-8"))
    print("Digest: |{}|".format(digest.hexdigest()))

    auth.send(digest.hexdigest())

    # Optional receiving and sending to client
    # So use timeout, so if client doesn't send anything, it will timeout
    data = "test"
    try:
        client.settimeout(1)
        data = client.recv(200)
    except:
        # timeout
        print("")
    if data != "test":
        print("Client: |{}|".format(data))
        val = findHost(data)
        if val != -1:
            hostName = hostList[val]
            ip = ipList[val]
            flag = flagList[val]
            finalHost = hostName + " " + ip + " " + flag
            print("finalHost: |{}|".format(finalHost))
            client.send(finalHost)
        if val == -1:
            print("NOT FOUND HERE!")
            # Hostname - Error:HOST NOT FOUND
            finalStr = data + " - Error:HOST NOT FOUND"
            print("finalStr: |{}|".format(finalStr))
            client.send(finalStr)


def findHost(data):
    print("findHost: |{}|".format(data))
    val = -1
    host = data.lower()
    if host in hostLowerList:
        val = hostLowerList.index(host)
        print("Found!")
    return val


if __name__ == "__main__":
    # Do all the things here!
    if(len(sys.argv) != 3):
        print("Wrong amount of arguments. Please follow syntax.")
        exit()

    key_query = getKey()
    auth = connectAS()
    client = connectClient()
    openFile()
    while(1):
        sendReceive(auth, client, key_query)

