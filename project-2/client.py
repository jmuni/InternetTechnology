# python client.py rsHostname rsListenPort


import threading
import time
import random

import socket
import sys

# List for everything that is going to be in the final RESOLVED.txt
finalList = []

# Connecting the RS server
def rsServer(hostName, port):
    portNumber = int(port)

    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    host_addr = socket.gethostbyname(hostName)

    # connect to the server on given host and port number
    server_binding = (host_addr, portNumber)
    rs.connect(server_binding)

    # getting data from server
    data_from_server=rs.recv(200)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # Client goes through the list to send messages to RS
    sendMessages(rs)

    # Close connection
    rs.close()


def sendMessages(rs):
    # Open file and read one line at a time
    f = open("PROJ2-HNS.txt", "r")
    print("Opening file: " + f.name)
    print("\n")
    f1 = f.readlines()

    # Send hostnames to RS or TS servers as needed

    for lines in f1:
        lines = lines.rstrip("\n")
        # Send line to RS to check first
        rs.send(lines.encode('utf-8'))
        print("-----------------------")
        print("Sent!")
        recvMessage(rs)


# Getting messages from RS server only.
def recvMessage(rs):
    data = rs.recv(200)
    temp = data.decode('utf-8')

    print("Found!: " + temp.strip())
    finalList.append(temp + "\n")
    print(temp)


if __name__ == "__main__":
    # all socket and networking things
    # parameters -- rsHostname and rsPortNumber
    rsServer(sys.argv[1], sys.argv[2])

    print("-------------------------------------")
    # Final Answer
    for x in finalList:
        print(x)
    print("-------------------------------------")

    listLen = len(finalList)


    # f = open("RESOLVED.txt", "w+")
    # for i in range(listLen):
    #     f.write(finalList[i])


    print("Done.")
