import json

def partition (amount, org_json):
	count = 0
	new_json = dict ()
	keys = list ()
	for key in org_json:
		if count == amount:
			break
		else:
			new_json [key] = org_json [key]
			keys.append (key)
			count += 1
	for key in keys:
		del org_json [key]
	return org_json, new_json

test = 25
dev = 25
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\Cleaned_Temp_Gen_PM_title_event_labels.json"
org_json = dict ()
with open (file_name, 'r') as reading:
	org_json = json.load (reading)

org_json, test_json = partition (test, org_json)
print ("test length: " + str (len (test_json)))
print ("org length: " + str (len (org_json)))
org_json, dev_json = partition (dev, org_json)
print ("dev length: " + str (len (dev_json)))
print ("org length: " + str (len (org_json)))
train_json = org_json

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\REE_TEST.json"
with open (file_name, 'w') as writing:
	json.dump (test_json, writing)
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\REE_dev.json"
with open (file_name, 'w') as writing:
	json.dump (dev_json, writing)
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\REE_train.json"
with open (file_name, 'w') as writing:
	json.dump (train_json, writing)
print ("DONE!!!")