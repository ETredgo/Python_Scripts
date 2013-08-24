__author__ = 'edtredgett - edtredgett@gmail.com'
#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys, re
import csv

print """
You must first save the HTML page for users twitter followers.
This script was quickly made in order to generate a CSV of a users, twitter followers, which can then be imported into Maltego for analysis :)
"""

fburl = sys.argv[1]
html = open(fburl, 'r')
filename = raw_input("Enter the filename to save the output to: ")
output_file = open(filename, 'w')
file_writer = csv.writer(output_file)

#Searches through the specified HTML document to find 'names' and saves them to a csv file
def fb_friends():
    count = 0
    holder = []
    print "Searching for all facebook friends.............."
    url = html
    bs = BeautifulSoup(url, "lxml")
    fb = bs.findAll('span', attrs={'class': 'username js-action-profile-name'})
    for line in fb:
	holder.append(re.findall(r'<span\b[^>]*>(.*?)</span>', str(line)))
    for follower in holder:
	count += 1
	file_writer.writerow(follower)
    print "\n%d users have been found"%count
    print "A list of the users found has been saved to " + filename + "\n"
  
if __name__ == "__main__":
    fb_friends()
    
