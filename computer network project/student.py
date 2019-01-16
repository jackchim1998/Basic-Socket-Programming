# -*- coding: cp950 -*-
# IERG3310 Project


import socket
import random
import time
import sys


robotVersion = "exp";
distPort = 3310;
socket.setdefaulttimeout(120)
distIP = '127.0.0.1'
localhost=''
studentid="1155094482"

print "Student version " + robotVersion + " started"
print "Creating TCP socket s1..."
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((distIP,distPort))
s1.send(studentid)
distPort2 = s1.recv(5)
print "receive distPort2: " + distPort2

print "Creating TCP socket s2..."
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((localhost, int(distPort2)))
listenSocket.listen(5)
print "Done"
print "\nTCP socket s2 created, ready for listening and accepting connection..."
print "Waiting for connection on port", distPort2
s2, address = listenSocket.accept()
studentIP = address[0]
print "\nClient from %s at port %d connected" %(studentIP,address[1])
listenSocket.close()
data = s2.recv(12)
print data + "string include 2 ports received"
data1 = int(data[:5])
data2 = data[6:]
data2 = int(data2[:5])
print "Creat a UDP socket to send random num"
num = random.randint(6,9)
print str(num) + " is sending"
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s3.bind((localhost,data2))
time.sleep(3)
s3.sendto(str(num),(distIP,data1))
while True:
	UDPmessage, address = s3.recvfrom(num*10)
	if int(UDPmessage)!=int(num):
		break
print str(UDPmessage) + " received"
for i in xrange(0,5):
	s3.sendto(str(UDPmessage),(distIP,data1))
	time.sleep(1)
	print "UDP packet %d sent"%(i+1)
default_buffersize=s2.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

while True:
        print "Please input buffer size(input 0 for default)（input END for ending）"
        bufsize = raw_input()
        if bufsize=="END":
                s1.send("END")
                break
        if int(bufsize) ==0:
                s2.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, int(default_buffersize))
        if int(bufsize) != 0:
                s2.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, int(bufsize))
        bufsize = s2.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        totalbytes=0
        numberofpackets=0
        print "The recving buffer size is "+str(bufsize)+" bytes"
        s1.send("bs"+str(bufsize))
        t=time.time()
        while True:
                testdata = s2.recv(bufsize)
                if(time.time()-t)>=10:
                        print "Number of receiving packets: "+str(numberofpackets)+" total received bytes: "+str(totalbytes)
                        t=time.time()
                if testdata=="END":
                        print "Number of receiving packets: "+str(numberofpackets)+" total received bytes: "+str(totalbytes)
                        break
                totalbytes=totalbytes+sys.getsizeof(testdata)
                numberofpackets+=1
        print "END"


s1.close()
s2.close()
s3.close()
exit()




