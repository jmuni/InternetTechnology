import threading
import time
import random
import sys
import socket 

TSHost = ""
TSHost_ip = ""

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

# If file exists, fill table and return
def fillTable():
    global TSHost
    global TSHost_ip
    table = {}
    try:
        textFile = "PROJI-DNSRS.txt"
        f = open(textFile,"r") 
        for line in f:
            line = line.strip()
            if line:
                temp = line.split()
                hostname, ip, flag = temp[0].lower(), temp[1], temp[2].upper()

                if flag == "NS":
                    TSHost = hostname
                    TSHost_ip = ip
                else:
                    table[hostname] = [ip,flag]
        return table
    except:
        print("[RS]: Error. File {} error".format(textFile))
        exit()
    finally:
        f.close()

def process(hostname,table):
    if hostname in table:
        ip = table[hostname][0]
        flag = table[hostname][1]
        return hostname+" "+ip+" "+flag
    elif TSHost:
        return TSHost + " " + TSHost_ip + " NS"

    return "skip"

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[RS]: Server socket successfully created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    port = checkPort(sys.argv[1])
    server_binding = ('', port) # (sys.argv)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[RS]: Server host name is: {}".format(host))
    host_ip = (socket.gethostbyname(host))
    print("[RS]: Server IP address is: {}".format(host_ip))
    print("[RS]: Waiting on Connection Request...")

    table = fillTable()
    maxSize = 200

    while True:
        client, address = ss.accept()
        print("[RS]: Connection request from client at: {}".format(address))
        try: 
            # Receive data/hostname from the client
            data_from_client = client.recv(maxSize).decode('utf-8')
            # Continous processing of data from client
            while data_from_client or 0:
                # Send data to client
                data = process(data_from_client, table)
                # Checks if TS server exists before processing request. If it doesnt, skip record
                print("[RS]: Client sent {} | Server sending {} to client {}".format(data_from_client,data, address))
                client.send(data.encode('utf-8'))
                # Wait for more data from client
                data_from_client = client.recv(maxSize).decode('utf-8')
            else: 
                client.close()
        except socket.error as err:
            client.close()
            print(err.args, err.message)

    ss.close()
    exit()

if __name__ == "__main__":
    if (len(sys.argv) > 2):
        print("Too many arguments. Check Syntax")
        print("python rs.py rsListenPort")
        exit()
    if (len(sys.argv) < 2):
        print("Too few arguments. Check Syntax")
        print("python rs.py rsListenPort")
        exit()
    tempThread = threading.Thread(name = 'server', target = server)

    tempThread.start()
