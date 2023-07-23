import json

def produce_grit (org_json):
	new_json = list ()
	i = 0
	for key in org_json:
		new_json.append (dict ())
		new_json [i] ["docid"] = key
		new_json [i] ["doctext"] = org_json [key] ["document"]
		new_json [i] ["extracts"] = dict ()
		for j in range (1, len (org_json [key] ["annotation"] [0]) + 1):
			new_json [i] ["extracts"] [str ("arg" + str (j))] = list ()
			new_json [i] ["extracts"] [str ("arg" + str (j))].append (list ())
			new_json [i] ["extracts"] [str ("arg" + str (j))] [0].append (list ())
			word = org_json [key] ["annotation"] [0] [str ("arg" + str (j))] [0]
			new_json [i] ["extracts"] [str ("arg" + str (j))] [0] [0].append (word)
			position = 0
			if (word == ""):
				continue
			else:
				position = org_json [key] ["document"].find (word) + 1
			new_json [i] ["extracts"] [str ("arg" + str (j))] [0] [0].append (position)
		i += 1
	return new_json

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\REE_TEST.json"
test_json = dict ()
with open (file_name, 'r') as reading:
	test_json = json.load (reading)
grit_test_json = produce_grit (test_json)
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\grit_test.json"
with open (file_name, 'w') as writing:
	json.dump (grit_test_json, writing)

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\REE_dev.json"
dev_json = dict ()
with open (file_name, 'r') as reading:
	dev_json = json.load (reading)
grit_dev_json = produce_grit (dev_json)
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\grit_dev.json"
with open (file_name, 'w') as writing:
	json.dump (grit_dev_json, writing)

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\REE_train.json"
train_json = dict ()
with open (file_name, 'r') as reading:
	train_json = json.load (reading)
grit_train_json = produce_grit (train_json)
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\grit_train.json"
with open (file_name, 'w') as writing:
	json.dump (grit_train_json, writing)
print ("DONE!!!")