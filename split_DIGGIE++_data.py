import json

file_name = "C:\\data\\DIGGIE++_input_titles.json"
json_strings = list ()
org_json_list = list ()
with open (file_name, 'r') as reading:
	json_strings = reading.readlines ()
for string in json_strings:
	if "\n" in string:
		#print ("contains endline character")
		new_string = string.replace ("\n", "")
		org_json_list.append (json.loads (new_string))
		continue
	org_json_list.append (json.loads (string))
#print (str (org_json_list))
test_list = list ()
dev_list = list ()
train_list = list ()
i = 0
for item in org_json_list:
	if i < 50:
		test_list.append (item)
	elif i < 100:
		dev_list.append (item)
	else:
		train_list.append (item)
	i += 1

# Print the lengths of each dataset
print (str (len (test_list)))
print (str (len (dev_list)))
print (str (len (train_list)))

test_string_list = list ()
for item in test_list:
	test_string_list.append (json.dumps (item) + "\n")

dev_string_list = list ()
for item in dev_list:
	dev_string_list.append (json.dumps (item) + "\n")

train_string_list = list ()
for item in train_list:
	train_string_list.append (json.dumps (item) + "\n")

# Write to files
file_name = "C:\\data\\test_DIGGIE++_input_titles2.json"
with open (file_name, 'w') as writing:
	writing.writelines (test_string_list)

file_name = "C:\\data\\dev_DIGGIE++_input_titles2.json"
with open (file_name, 'w') as writing:
	writing.writelines (dev_string_list)

file_name = "C:\\data\\train_DIGGIE++_input_titles2.json"
with open (file_name, 'w') as writing:
	writing.writelines (train_string_list)
print ("DONE!!!")