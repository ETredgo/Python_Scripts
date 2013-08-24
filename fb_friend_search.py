__author__ = 'Ed Tredgett - edtredgett@gmail.com'
#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys
import csv

print """In order to use this tool you must first save the HTML page of the users friends list.
This script was wrote in order to import the CSV into maltego for analysis :)
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
    fb = bs.findAll('div', attrs={'class': 'fsl fwb fcb'})
    for line in fb:
    	holder.append(line.find('a').get_text())
    for name in holder:
	file_writer.writerow([name.encode('ascii','ignore')])
	count += 1
    print "\nThe user has %d friends."%count
    print "\nA list of all their friends has been saved to " + filename + "\n"

if __name__ == "__main__":
    fb_friends()
    
