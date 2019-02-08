#!/usr/bin/python3
## Jess, Jan 30, 2019, iteration-rewrite
## iteration example is adapted from the dataverse API documentation, iteration only needed if results >1000

## example of pulling all the metadata from datasets below X dataverse

import json
import requests 

dataverse_server="demodv.scholarsportal.info" 
api_key="" # not needed for accessing dataset metadata on demodv, needed for live

rows = 1000
start = 0 
page = 1 
condition = True
while (condition):
	dataset_URL = "https://%s/api/search?q=*&type=dataset&start=" % (dataverse_server) + str(start) + "&per_page=1000" # search dataverse_server for all types=dataset, get 1000 results (the max), and set the start point for iteration
	returned_datasets = requests.get(url = dataset_URL) # make call
	returned_datasets = json.loads(returned_datasets.text) # load response as json
	total = returned_datasets['data']['total_count'] # get the total number returned
	for i in returned_datasets['data']['items']: # iterate over the returned datasets
		print(" - ", i['name'],"(" + i['type'] + ")," + i['global_id']) # prints info to screen for testing, not necessary
		metadataURL="http://%s/api/datasets/export?exporter=dataverse_json&persistentId=%s " % (dataverse_server,(i['global_id'])) # construct URL according to API docs at http://guides.dataverse.org/en/latest/api/native-api.html#id40
		dataset_metadata = requests.get(url = metadataURL) # make call
		data = json.loads(dataset_metadata.text) # load response as json
		with open('data.json', 'a') as outfile: # with data.json open in append mode
			json.dump(data, outfile, sort_keys=True, indent=4) # dump the json response, sorted, formatted nice
	start = start + rows # add # of rows, was set to 1000
	page += 1 # increase page #
	print("total datasets found:", total)
	condition = start < total # if start < total number of datasets, repeat)
