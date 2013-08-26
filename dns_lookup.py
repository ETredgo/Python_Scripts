#!/usr/bin/env python
__author__ = "Ed Tredgett - Logically Secure"
#Script to get whois data and push to csv file
#Created in order to use exported urls from a pcap,
#then import the csv which is generated into maltego for analysis

try:
	import whois
	import sys
	import csv
except:
	import sys
	print """
Ensure you have the python whois module installed.
It can be retrieved by entering: pip install python-whois
If you don't have pip installed run: sudo apt-get install python-pip
	"""
	sys.exit(1)

def dns_list():
	fdesc = open(domains_perm, 'r')
	lines = [line.strip() for line in open(domains_perm)]
	for line in lines:
		print line
		try: w = whois.whois(line)
		except: 
			print "Error with url: " + str(line)
			pass
		url = w.domain_name
		if url == []: continue
		else:
			url = line
			cdate = str(w.creation_date).split(' ')[0]
			if "datetime" in cdate:
				cdate = str(w.creation_date[0]).split(' ')[0]
			else: pass
			if cdate == "[]": cdate = "Not Available"
			else: pass	
			try: udate = str(w.updated_date).split(' ')[0]
			except: 
				try:
					udate = str(w.updated_date).split(' ')[0]
				except:
					udate = "Not Available"
			if "datetime" in udate:
				udate = str(w.updated_date[0]).split(' ')[0]
			else: pass
			if "['" in udate:
				udate = str(w.updated_date[0]).split(' ')[0]
			else: pass
			if udate == "[]": udate = "Not Available"
			else: pass
			try:
				email = str(w.registrant_name)
				if "[" in email:
					email = w.registrant_name[0]
				else: pass
			except:
				try:
					email_list = [w.emails]
					email = email_list[0][0]
					if "@" in email:
						pass
					else:
						email = email_list[0]
				except:
					try:
						email = w.registrant
						print "Trying registrant"
					except:
						email = "Not Available"
			if email == "[]": email = "Not Available"
			else: pass
			writer.writerow([url,cdate,udate,email])
	myfile.close()
	
if __name__ == "__main__":
	try:
		domains_perm = sys.argv[1]
	except:
		print "\nUsage: ./dns_lookup.py [File with list of domains]\n"
		sys.exit(1)
	csv_file = raw_input("Enter output file name: ")
	myfile = open(csv_file, "wb")
	writer = csv.writer(myfile)
	cheaders = ["URL","Creation Date", "Update Date", "Email/Registrant"]
	writer.writerow(cheaders)
	dns_list()
