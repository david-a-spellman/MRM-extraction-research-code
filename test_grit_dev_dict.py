import json

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\grit_dev.json"
dev_json = dict ()
with open (file_name, 'r') as reading:
	dev_json = json.load (reading)
for i in range (0, len (dev_json)):
	for role in dev_json [i] ["extracts"]:
		for entity in dev_json [i] ["extracts"] [role]:
				continue

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\grit_test.json"
test_json = dict ()
with open (file_name, 'r') as reading:
	test_json = json.load (reading)
for i in range (0, len (test_json)):
	for role in test_json [i] ["extracts"]:
		for entity in test_json [i] ["extracts"] [role]:
				continue

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\grit_train.json"
train_json = dict ()
with open (file_name, 'r') as reading:
	train_json = json.load (reading)
for i in range (0, len (train_json)):
	for role in train_json [i] ["extracts"]:
		for entity in train_json [i] ["extracts"] [role]:
				continue