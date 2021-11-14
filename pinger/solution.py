from socket import *
import os
import sys
import struct
import time
import select
import binascii
from statistics import stdev
# Should use stdev

ICMP_ECHO_REQUEST = 8


def checksum(string):
   csum = 0
   countTo = (len(string) // 2) * 2
   count = 0

   while count < countTo:
       thisVal = (string[count + 1]) * 256 + (string[count])
       csum += thisVal
       csum &= 0xffffffff
       count += 2

   if countTo < len(string):
       csum += (string[len(string) - 1])
       csum &= 0xffffffff

   csum = (csum >> 16) + (csum & 0xffff)
   csum = csum + (csum >> 16)
   answer = ~csum
   answer = answer & 0xffff
   answer = answer >> 8 | (answer << 8 & 0xff00)
   return answer



def receiveOnePing(mySocket, ID, timeout, destAddr):
   timeLeft = timeout

   while 1:
       startedSelect = time.time()
       whatReady = select.select([mySocket], [], [], timeLeft)
       howLongInSelect = (time.time() - startedSelect)
       if whatReady[0] == []:  # Timeout
           return "Request timed out."

       timeReceived = time.time()
       recPacket, addr = mySocket.recvfrom(1024)

       # Fill in start
       # print(int.from_bytes(recPacket, byteorder='big'))

       # Fetch the ICMP header from the IP packet
       if recPacket:
           ip_packet = struct.unpack_from('!BBHHHBHII', recPacket, 0)
           icmp_packet = struct.unpack_from('bbHHh', recPacket, 20)
           return [f'Reply from {addr[0]}: bytes={len(recPacket)} time={str(round((timeReceived-startedSelect)*1000,7))}ms TTL={ip_packet[5]}',(timeReceived-startedSelect)*1000]

       # Fill in end
       timeLeft = timeLeft - howLongInSelect
       if timeLeft <= 0:
           return ["Request timed out.",0]


def sendOnePing(mySocket, destAddr, ID):
   # Header is type (8), code (8), checksum (16), id (16), sequence (16)

   myChecksum = 0
   # Make a dummy header with a 0 checksum
   # struct -- Interpret strings as packed binary data
   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   data = struct.pack("d", time.time())
   # Calculate the checksum on the data and the dummy header.
   myChecksum = checksum(header + data)

   # Get the right checksum, and put in the header

   if sys.platform == 'darwin':
       # Convert 16-bit integers from host to network  byte order
       myChecksum = htons(myChecksum) & 0xffff
   else:
       myChecksum = htons(myChecksum)


   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   packet = header + data

   mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


   # Both LISTS and TUPLES consist of a number of objects
   # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
   icmp = getprotobyname("icmp")


   # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
   mySocket = socket(AF_INET, SOCK_RAW, icmp)

   myID = os.getpid() & 0xFFFF  # Return the current process i
   sendOnePing(mySocket, destAddr, myID)
   delay = receiveOnePing(mySocket, myID, timeout, destAddr)
   mySocket.close()
   return delay


def ping(host, timeout=1):
   # timeout=1 means: If one second goes by without a reply from the server,      # the client assumes that either the client's ping or the server's pong is lost
   dest = gethostbyname(host)
   print("Pinging " + dest + " using Python:")
   print("")
   # Calculate vars values and return them
   # Send ping requests to a server separated by approximately one second
   delays = []
   for i in range(0,4):
       delay = doOnePing(dest, timeout)
       print(delay[0])
       delays.append(delay[1])
       time.sleep(1)  # one second
   print ('\n'+f'--- {host} ping statistics ---')
   print(f'4 packets transmitted, {4-delays.count(0)} packets received, {str(round(delays.count(0)/4, 4))}% packet loss')
   vars = [str(round(min(delays),2)), str(round(sum(delays)/4,2)), str(round(max(delays),2)),str(round(stdev(delays),2))]
   print(f'rount-trip min/avg/max/stddev = {vars[0]}/{vars[1]}/{vars[2]}/{vars[3]} ms')
   return vars

if __name__ == '__main__':
   ping("localhost")
   ping("no.no.e")
   ping("google.co.il")
