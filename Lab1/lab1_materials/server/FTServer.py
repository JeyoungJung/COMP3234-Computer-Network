#!/usr/bin/python3

import socket
import sys

def main(argv):
    # get port number from argv
    serverPort = int(argv[1])
   
    # create socket and bind
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sockfd.bind( ("", serverPort) )
    
    sockfd.listen()
    
    print("The server is ready to receive")
    
    while True:
        
        # accept new connection
        conn, addr = sockfd.accept() 

        # receive file name/size message from client  
        try:       
            sentence = conn.recv(1024)
        except socket.error as err:
            print("Recv error: ", err)
        
        #use Python string split function to retrieve file name and file size from the received message
        if sentence:
            sentence = sentence.decode('utf-8')
            fname, filesize = sentence.split(":")
        
            print("Open a file with name \'%s\' with size %s bytes" % (fname, filesize))
            
            #create a new file with fname
        
            fd = open(fname, 'wb')
        
            remaining = int(filesize)

            conn.send(b"OK")


            print("Start receiving . . .")
            while remaining > 0:
                # receive the file content into rmsg and write into the file
                rmsg = conn.recv(remaining)
                fd.write(rmsg)
                remaining -= len(rmsg)

            print("[Completed]")
            fd.close()

        else:
            print("Connection is broken")

        conn.close()
        
    sockfd.close()        

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 FTServer.py <Server_port>")
        sys.exit(1)
    main(sys.argv)