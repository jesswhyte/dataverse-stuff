#!/usr/bin/python3
###BEFORE YOU RUN, UPDATE THE VARIABLES BELOW
#to run: python createDV-uploadfile.py <directory you want to make dataset out of>

#If you want this script to iterate through subdirectories, try embedding contens in a for loop, e.g. 
#for dir in next(os.walk('.'))[1]: #assumes running script from top-level ICICLE directory)
#could be dangerous if there's a fail or error 

import os
from subprocess import Popen, PIPE, STDOUT, call, run
import xml.etree.ElementTree as ET # importing ElementTree as ET, so I don't have to type it out a bunch
import re # import editor for string fixing/replacing
import sys
dir = sys.argv[1] # dir = directory variable you pass as argument, e.g. /Documents/ICICLES/120123_atlas

# --------------------------------------------------
# UPDATE the 3 variables below to run this script 
# --------------------------------------------------
dataverse_server="https://demodv.scholarsportal.info" #demodv is the Scholar's Portal sandbox, update to your server
api_key="<your API key goes here>" #to get api key, create acct on dataverse, go to API Token, Create Token
dataverse_id="<your dataverse ID goes here>" #you must create a dataverse first, easiest to do this in online GUI


###function to upload individual file to KNOWN dataset
def upload(file, description):
	print ("\nAbout to upload: %s" % (file)) # print for TESTING
	cmd = "curl -H \"X-Dataverse-key:%s\" -X POST -F \'file=@%s\' -F \'jsonData={\"description\":\"%s\",\"categories\":[\"Data\"]}\' \"%s/api/datasets/:persistentId/add?persistentId=%s\" " % (api_key, file, description, dataverse_server, dataset_id) # constructs icon upload command
	print ("\nAbout to send following command: %s\n" % (cmd)) #print icon upload command, just for TESTING
	os.system(cmd) #run the icon upload command, should really do this using request module or subprocess, but this works

### find the atom.xml,
### NOTE: assumes there is an atom.xml, change below to match wherever your atom.xml is stored
xml = os.path.join(dir,+"atom.xml") # make variable out of atom.xml file,  
print ("XML to upload: %s" % (xml)) # print xml - just for TESTING

### construct command to create dataset on dataverse
cmd = "curl -u '%s': --data-binary \"@%s\" -H \"Content-Type: application/atom+xml\" %s/dvn/api/data-deposit/v1.1/swordv2/collection/dataverse/%s" % (api_key, xml, dataverse_server, dataverse_id) # constructs the command needed to create dataset using corresponding xml
print ("About to send following command to Dataverse SWORD API: %s" % (cmd)) # print the command, just for TESTING

### run the command to create icicle dataset on dataverse
result = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True,universal_newlines=True).communicate()[0] # run command as subprocess

### get the dataset_id from the command response
dataset = ET.fromstring(result) # dataset = parsed xml response from post command
for idnode in dataset.findall('.//{http://www.w3.org/2005/Atom}id'):  
	dataset_id = idnode.text #create dataset_id variable from the idnode
	dataset_id = re.sub(r'.*doi:','doi:', dataset_id) #strip out everything before the doi
	print ("\nFound dataset_id: %s" % dataset_id) # print dataset_id for TESTING

### Example of how to upload a file to dataset just created, note: uses NATIVE API:
icon = os.path.join(dir,"icon.jpg") # make variable for file
description = "the icon jpg file" # construct the descriptor 
upload(icon,description) #upload(file, description)


