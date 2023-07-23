import json

file_name = "C:\\users\\david\\projects\\tempgen\\data\\muc34\\proc_output\\dev.json"
org_json = dict ()
with open (file_name, 'r') as reading:
	org_json = json.load (reading)
print (len (org_json))