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

# If the DNS file exists, fill the table with hostname,ip,flag and return
def fillTable():
    table = {}
    try:
        file_name = "PROJ2-DNSTSedu.txt"
        f = open(file_name,"r") 
        for line in f: 
            temp = line.split()
            hostname, ip, flag = temp[0].lower(), temp[1], temp[2].upper()
            table[hostname] = [ip,flag]
        return table
    except:
        print("[TS_EDU]: File {} not found".format(file_name))
    finally:
        f.close()

# Check to see if hostname is in table
def checkTable(hostname,table):
    if hostname in table:
        return hostname + " " + table[hostname][0] + " " + table[hostname][1]
    else:
        return hostname + " - " + "Error:HOST NOT FOUND"

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS_EDU]: TS Socket sucessfully created")
    except socket.error as err:
        print('[TS_EDU]: socket open error: {}\n'.format(err))
        exit()
    binding = ('', checkPort(sys.argv[1]))
    ss.bind(binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[TS_EDU]: Host name : {}".format(host))
    host_ip = (socket.gethostbyname(host))
    print("[TS_EDU]: IP address : {}".format(host_ip))
    print("[TS_EDU]: Waiting on Connection Request...")
 
    dns_table = fillTable()
    maxSize = 200

    while True:
        client, address = ss.accept()
        print("[TS_EDU]: Connection request from client {}".format(address))
        try: 
            clientdata = client.recv(maxSize).decode('utf-8')
            while clientdata or 0:
                data = checkTable(clientdata, dns_table)
                print("[TS_EDU]: Client sent {} | Server sending {} to client {}".format(clientdata,data, address))
                client.send(data.encode('utf-8'))
                clientdata = client.recv(maxSize).decode('utf-8')
            else: 
                client.close()
        except socket.error as err:
            client.close()
            print(err.args, err.message)

    print("[TS_EDU]: Socket Connection Closed")	
    ss.close()
    exit()

if __name__ == "__main__":
    if (len(sys.argv) > 2):
        print("Too many arguments. Check Syntax")
        print("python ts_edu.py tsListenPort")
        exit()
    if (len(sys.argv) < 2):
        print("Too few arguments. Check Syntax")
        print("python ts_edu.py tsListenPort")
        exit()
    
    tempThread = threading.Thread(name = 'server', target = server)
    tempThread.start()