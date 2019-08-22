import threading
import time
import random
import sys

import socket

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

# Populate and return a table if DNS file exists.
def fillTable():
    table = {}
    try:
        file_name = "PROJI-DNSTS.txt"
        f = open(file_name,"r") 
        for line in f: 
            temp = line.split()
            hostname, ip, flag = temp[0].lower(), temp[1], temp[2].upper()
            table[hostname] = [ip,flag]
        return table
    except:
        print("[TS]: File {} not found".format(file_name))
    finally:
        f.close()

# Check to see if hostname is in table
def process_query(hostname,table):
    if hostname in table:
        ip = table[hostname][0]
        flag = table[hostname][1]
        return hostname + " " + ip + " " + flag
    else:
        return hostname + " - " + "Error:HOSTNOTFOUND"

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS]: TS Socket sucessfully created")
    except socket.error as err:
        print('[TS]: socket open error: {}\n'.format(err))
        exit()
    port = checkPort(sys.argv[1])
    server_binding = ('', port)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[TS]: Host name : {}".format(host))
    host_ip = (socket.gethostbyname(host))
    print("[TS]: IP address : {}".format(host_ip))
    print("[TS]: Waiting on Connection Request...")
 
    dns_table = fillTable()
    maxSize = 200

    while True:
        client, address = ss.accept()
        print("[TS]: Connection request from client {}".format(address))
        try: 
            # Receive data/hostname from the client
            data_from_client = client.recv(maxSize).decode('utf-8')
            # Continous processing of data from client
            while data_from_client or 0:
                # Send data to client
                data = process_query(data_from_client, dns_table)
                print("[TS]: Client sent {} | Server sending {} to client {}".format(data_from_client,data, address))
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
        print("python ts.py tsListenPort")
        exit()
    if (len(sys.argv) < 2):
        print("Too few arguments. Check Syntax")
        print("python ts.py tsListenPort")
        exit()
    
    tempThread = threading.Thread(name = 'server', target = server)

    tempThread.start()