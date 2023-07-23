import json

file_name = "C:\\data\\Temp_Gen_no_arg4_new_triggers.json"
org_json = dict ()
with open (file_name, 'r') as reading:
	org_json = json.load (reading)
new_json = dict ()
for key in org_json:
	del org_json [key] ["annotation"] [0] ["MESSAGE-TEMPLATE"]
	for i in range (0, len (org_json [key] ["annotation"] [0])):
		org_json [key] ["annotation"] [0] ["arg" + str (i + 1)] = [org_json [key] ["annotation"] [0] ["arg" + str (i + 1)]]
new_json = org_json
file_name = "C:\\data\\Cleaned_Temp_Gen_no_arg4_new_triggers.json"
with open (file_name, 'w') as writing:
	json.dump (new_json, writing)
print ("done")