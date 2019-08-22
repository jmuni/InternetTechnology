import threading
import time
import random
import sys 

import socket

#Check for valid port number
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

# Gather list of hostname strings to send to server(s)
def hostList():
    hostList = []
    f = open("PROJI-HNS.txt","r") 
    for line in f:
        hostList.append(line.strip().lower())
    return hostList

# Modularizing .split() function for usage
def organize(data):

    temp = data.split()
    hostname, ip, flag = temp[0].lower(), temp[1], temp[2].upper()
    #ip = temp[1]
    #flag = temp[2]
    arr = []
    arr = [hostname,ip,flag]
    return arr

# Writes resolved hosts to file_name
def output(hosts):
    try:
        textFile = "./RESOLVED.txt"
        f = open(textFile, 'w+')
        for host in hosts:
            f.write("{}\n".format(host))
        f.close()
    except:
        print("[C]: Error writing to {}".format(textFile))
    finally:
        f.close()

# Run Client
def client():
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket to DNSRS created")
    except socket.error as err:
        print("[C]: socket open error: {} \n".format(err))
        exit()
    # Gather fields from user
    rsHostName, rsListenPort,  tsListenPort = sys.argv[1], checkPort(sys.argv[2]), checkPort(sys.argv[3])
    #rsListenPort = checkPort(sys.argv[2])
    #tsListenPort = checkPort(sys.argv[3])
    # Connect to the server on local machine
    addr = socket.gethostbyname(rsHostName)
    binding = (addr, rsListenPort)
    print("[C]: Connecting to RS host: {} {}".format(rsHostName,binding))
    rs.connect(binding)
    # Send message(s) to server
    hostnames = hostList()
    maxSize = 200 
    resolveds = []
    for host in hostnames:
        print("[C]: Sending {} to RS".format(host))
        rs.send(host.encode('utf-8'))
        try: 
            data = rs.recv(maxSize).decode('utf-8')
            print("[C]: Received {} from RS".format(data))
            if (data != "skip"):

                info = organize(data)
                ret_host, ret_ip, ret_flag = info[0], info[1], info[2]
                #ret_ip = info[1]
                #ret_flag = info[2]
                # Append to resolved file or proceed to ask TS
                if ret_flag == "A":
                    resolveds.append(ret_host + " "  +ret_ip + " " + ret_flag)
                elif ret_flag == "NS": #if not resolved, open TS socket
                    try:
                        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        print("[C]: Client socket to DNSTS created")
                    except socket.error as err:
                        print("[C]: socket open error: {} \n".format(err))
                        exit()
                    # Connect to the server on local machine
                    if ret_ip == "-":
                        ts_addr = socket.gethostbyname(ret_host)
                    else:
                        ts_addr = ret_ip
                    print (ret_ip)
                    ts_binding = (ts_addr, tsListenPort)
                    print("[C]: Connecting to TS host: {} {}".format(ret_host,ts_binding))
                    ts.connect(ts_binding)
                    # Send TS host to resolve
                    print("[C]: Sending {} to TS".format(host))
                    ts.send(host.encode('utf-8'))
                    # Receive data from TS
                    data = ts.recv(maxSize).decode('utf-8')
                    print("[C]: Received: {}".format(data))
                    # Format for easy access 0 = host, 1 = ip, 2 = flag
                    info = organize(data)
                    # Add remaining data to resolved file
                    if info[2] == "Error:HOSTNOTFOUND":
                        info[2] = "Error:HOST NOT FOUND"
                    resolveds.append(info[0] + " "  + info[1] + " " + info[2])
        
                    ts.close()
                    print("[C]: Client socket closed")
            else:
                print("[RS]: Error. TS server not found to process {}".format(host))
        except socket.error as err:
            print("[C]: Network error: {} \n".format(err))
    output(resolveds)      

    rs.close()
    print("[C]: Client socket to DNSRS closed")
    exit()

if __name__ == "__main__":
    if (len(sys.argv) > 4):
        print("Too many arguments. Check Syntax")
        print("python client.py rsHostname rsListenPort tsListenPort")
        exit()
    if (len(sys.argv) < 4):
        print("Too few arguments. Check Syntax")
        print("python client.py rsHostname rsListenPort tsListenPort")
        exit()
    tempThread = threading.Thread(name = 'client', target = client)

    tempThread.start()
