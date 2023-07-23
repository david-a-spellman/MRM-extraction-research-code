import json

file_name = "C:\\data\\PM_title_event_labels.json"
org_json = dict ()
with open (file_name, 'r') as reading:
	org_json = json.load (reading)
new_json = dict ()
for key in org_json:
	new_json [key] = dict ()
	for i in range (0, len (org_json [key])):
		if (i == 0):
			new_json [key] ["document"] = org_json [key] [i]
		elif (i == 1):
			continue
		else:
			new_json [key] ["annotation"] = list ()
			new_json [key] ["annotation"].append (dict ())
			new_json [key] ["annotation"] [0] ['MESSAGE-TEMPLATE'] = '1'
			for j in range (1, len (org_json [key] [i]) + 1):
				new_json [key] ["annotation"] [0] [str ("arg" + str (j))] = org_json [key] [i] [j - 1]
file_name = "C:\\data\\Temp_Gen_PM_title_event_labels.json"
with open (file_name, 'w') as writing:
	json.dump (new_json, writing)
print ("done")