import subprocess
from subprocess import Popen
from subprocess import PIPE
import sys
import shlex
import time
import os
import platform
import shutil

def doesItExist(command, name, sectionNumber ) :
	'''handle duplicates due to similar spellings, avoid using regular expressions'''
	result, err, exitcode = call(command)
	#print("result="+result + " err="+err+"enderr")
	if ( err != "") :
		return False

	rows = result.split('\n')
	for row in rows:
		#print("row=" +row)
		existingSection = row.split(" ")[sectionNumber]
		#print("existingSection"+existingSection)
		if existingSection == name :
			return True

def call(cmd):
	"""Runs the given command locally and returns the output, err and exit_code, handles Pipes."""
	if "|" in cmd:
		cmd_parts = cmd.split('|')
	else:
		cmd_parts = []
		cmd_parts.append(cmd)
	i = 0
	p = {}
	for cmd_part in cmd_parts:
		#print(cmd_part)
		cmd_part = cmd_part.strip()
		if i == 0:
		  p[i]=Popen(shlex.split(cmd_part),stdin=None, stdout=PIPE, stderr=PIPE)
		else:
		  p[i]=Popen(shlex.split(cmd_part),stdin=p[i-1].stdout, stdout=PIPE, stderr=PIPE)
		i = i +1
	(output, err) = p[i-1].communicate()
	exit_code = p[0].wait()

	return str(output).strip(), str(err), exit_code

""""""""""""""""" Main program starts here """""""""""""""""
system = platform.system()
if ( system == "Windows"):
	statementStatus  = subprocess.call("cls", shell=True)
else:
	statementStatus  = subprocess.call("reset", shell=True)

import os
hostname = os.uname()[1]
tutorialFile="hello-world"
tutorialName="Hello World"
gitRepo="Predix-HelloWorld-WebApp"

print ("$ Welcome to Predix")

""""""""""""""""" Dropbox """""""""""""""""
if hostname == "predix-devbox" :
	print ("$ Would you to like save your work in your Dropbox account?")
	print ("1. Yes")
	print ("2. No thanks")
	choice = raw_input("$")
	if choice == "1" :
		dropbox=True
		print("Okay, do you agree to the EULA located at /predix/Dropbox/predix-dropbox-eula.txt?.")
		print ("1. Yes")
		print ("2. No")
		choice = raw_input("$")
		if choice == "1" :
			dropbox=True
			statementStatus  = subprocess.call("killall -q dropbox", shell=True)
			statementStatus  = subprocess.call("./.dropbox-dist/dropboxd&", shell=True)
			print("Dropbox daemon started")
			print("")
			raw_input("Press Enter to continue...")
			statementStatus  = subprocess.call("reset", shell=True)
		elif choice == "2" :
			print("Okay, we won't start the dropbox daemon.")
			print("We'll put your work in /predix/dropbox in case you change your mind.")
			print("To launch the Dropbox daemon enter: ./predix/.dropbox-dist/dropboxd")
			print("")
			raw_input("Press Enter to continue...")
			statementStatus  = subprocess.call("reset", shell=True)
		else :
			system.exit("Sorry, I did not understand. To restart the script enter: python " + turorialFile + ".py ")
	elif choice == "2" :
		print("Okay, we'll put your work in /predix/dropbox in case you change your mind.")
		print("To launch the Dropbox daemon enter: ./predix/.dropbox-dist/dropboxd")
		print("")
		raw_input("Press Enter to continue...")
		statementStatus  = subprocess.call("reset", shell=True)
	else :
		system.exit("Sorry, I did not understand. To restart the script enter: python " + turorialFile + ".py ")

print ("$ Welcome to Predix")
print ("$ Would you to like me to walk you through " + tutorialName + "?")
print ("1. Yes, walk me through it")
print ("2. Actually, I want to do the steps myself.")
choice = raw_input("$")
if choice == "1" :
    print("")
elif choice == "2" :
	print("Okay, follow the instructions in the " + tutorialName + " tutorial (https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1475).  Good Luck!")
	print("To restart the script enter: python " + tutorialFile + ".py")
	print("")
	sys.exit()
else :
	system.exit("Sorry, I did not understand. To restart the script enter: python " + tutorialFile + ".py ")
	print("")

time.sleep(1)

""""""""""""""""" Check for Network """""""""""""""""
print("Let's see if you can get to the internet")
result, err, exitcode = call('curl google.com')
# print("result="+result + " err="+err+"enderr", "exitcode=")
# print(exitcode)
if exitcode >= 1 :
	sys.exit("Internet access not found.  Are you behind a proxy?  If so, set environment variables, e.g. HTTP_PROXY=http://myproxy.mycompany.com:8080, HTTPS_PROXY=$HTTP_PROXY.  Or perhaps you left the office and need to unset the environment variables, e.g. unset HTTP_PROXY, etc.")
print("Internet access successful")
print("")
time.sleep(1.5)

""""""""""""""""" Check for Github """""""""""""""""
print("Let's see if you can download from GitHub")
try:
	result, err, exitcode=call("git --version")
except:
	sys.exit("GIT CLI does not exist, please install it.  Visit the Development Environment tutorials.  (https://www.predix.io/resources/tutorials/journey.html#1607) ")
print("Success, you have the Git CLI")
print("")
time.sleep(1.5)

""""""""""""""""" Check for CF CLI """""""""""""""""
print("Let's see if you have the Cloud Foundry CLI")
try:
	result, err, exitcode=call('cf --version')
except:
	sys.exit("Cloud Foundry CLI does not exist, please install it.  Visit the Development Environment tutorials.  (https://www.predix.io/resources/tutorials/journey.html#1607) ")
print("Success, you have the Cloud Foundry CLI")
print("")
time.sleep(1.5)

""""""""""""""""" Check for Predix Plugin """""""""""""""""
print("Let's see if you have the Predix CLI Plugin")
result, err, exitcode=call('cf plugins')
if not "Predix" in result :
    print("installing the Predix plugin for the Cloud Foundry cli")
    if system == "Windows" :
        statementStatus  = subprocess.call("cf install-plugin https://github.com/PredixDev/cf-predix/releases/download/1.0.0/predix_win64.exe", shell=True)
    elif system == "Darwin" :
        statementStatus  = subprocess.call("cf install-plugin https://github.com/PredixDev/cf-predix/releases/download/1.0.0/predix_osx", shell=True)
    elif system == "Linux" :
        statementStatus  = subprocess.call("cf install-plugin https://github.com/PredixDev/cf-predix/releases/download/1.0.0/predix_linux64", shell=True)
    else :
        system.exit("sorry, I did not understand")
print("Success, you have the Predix CLI")
print("")
time.sleep(1.5)

""""""""""""""""" Check for Lggin """""""""""""""""
print("Let's see if you need to login in to the Predix Cloud")
result, err, exitcode=call('cf target')
if "Not logged in" in result:
    print("Let's log in to Cloud Foundry")
    statementStatus  = subprocess.call("cf predix", shell=True)
    if statementStatus == 1 :
    	print("Error logging in to CF")
    print("")
else:
    print "Great, you are already logged in"
print("")
time.sleep(1.5)

""""""""""""""""" Github """""""""""""""""
print("Let's copy " + tutorialName + " to your machine")
print ('git clone https://github.com/PredixDev/' + gitRepo + '.git')
print("")
print(system)
if system == "Windows" :
	if os.path.exists(gitRepo):
		os.system("rmdir /S /Q " + gitRepo)
	statementStatus  = subprocess.call('git clone https://github.com/PredixDev/' + gitRepo + '.git', shell=True)
elif system == "Darwin" :
	if os.path.exists(gitRepo):
		statementStatus  = subprocess.call("rm -rf " + gitRepo)
	statementStatus  = subprocess.call('git clone https://github.com/PredixDev/' + gitRepo + '.git', shell=True)
else:
	print('For linux we assume you are on a DevBox and will place the app in /predix/Dropbox')
	if os.path.exists("/predix/Dropbox/" + gitRepo):
		statementStatus  = subprocess.call("rm -rf /predix/Dropbox/" + gitRepo, shell=True)
	statementStatus  = subprocess.call('cd /predix/Dropbox; git clone https://github.com/PredixDev/' + gitRepo + '.git', shell=True)
	result = subprocess.call('rm -rf ' + gitRepo,shell=True)
# print("result="+result + " err="+err+"enderr", "exitcode=")
# print(exitcode)
if statementStatus == 1 :
	sys.exit("Unable to git clone the project")
print("")
time.sleep(1.5)

""""""""""""""""" Push """""""""""""""""
print("Please push " + tutorialName + " to the cloud.  Give it a unique name or it won't be able to hand out a URL for your app. ")
print("e.g. enter:  cf push <my-unique-name>")
choice = raw_input("$")
if system == "Windows" :
	statementStatus  = subprocess.call("cd " + gitRepo + " & " + choice, shell=True)
elif system == "Darwin" :
	statementStatus  = subprocess.call("cd " + gitRepo + ";" + choice, shell=True)
else:
	statementStatus  = subprocess.call("cd /predix/Dropbox/" + gitRepo + ";" + choice, shell=True)
# print("result="+result + " err="+err+"enderr", "exitcode=")
# print(exitcode)
if statementStatus == 1 :
	sys.exit("unable to push your app to the cloud")
print("")

""""""""""""""""" Wrap it up """""""""""""""""
print("Now that it's uploaded to the cloud, look for the 'urls:' entry above, copy that to your browser ")
print("and put https:// in front of it")
print ("Once you see Hello World in the browser, you have completed the " + tutorialName + " interactive tutorial.")
