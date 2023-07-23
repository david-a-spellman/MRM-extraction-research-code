import json

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\grit_dev.json"
dev_json = dict ()
with open (file_name, 'r') as reading:
	dev_json = json.load (reading)
print (type (dev_json))