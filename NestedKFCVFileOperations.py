import os
import json

def make_fold_files (folds, directory):
	file_list = list ()
	if not os.path.isdir (directory):
		os.mkdir (directory)
	for i in range (0, len (folds)):
		fold_string_list = list ()
		for item in folds [i]:
			fold_string_list.append (json.dumps (item) + "\n")
		file_name = str (directory + "fold_" + str (i + 1) + ".json")
		with open (file_name, 'w') as writing:
			writing.writelines (fold_string_list)
		file_list.append (file_name)
	return file_list

def make_temp_train_file (train_files, directory):
	train_string_list = list ()
	if not os.path.isdir (directory):
		os.mkdir (directory)
	for file_name in train_files:
		json_strings = list ()
		with open (file_name, 'r') as reading:
			json_strings = reading.readlines ()
		for string in json_strings:
			train_string_list.append (string)
	file_name = str (directory + "temp_training_data.json")
	with open (file_name, 'w') as writing:
		writing.writelines (train_string_list)
	return file_name

def modify_jsonnet_file (jsonnet_file, train, dev, test):
	jsonnet_strings = list ()
	output = list ()
	with open (jsonnet_file, 'r') as reading:
		jsonnet_strings = reading.readlines ()
	for line in jsonnet_strings:
		if "train: " in line:
			temp1 = line.split ("\"") [0]
			temp2 = line.split ("\"") [2]
			output.append (str (temp1 + "\"" + train + "\"" + temp2))
		elif "validation: " in line:
			temp1 = line.split ("\"") [0]
			temp2 = line.split ("\"") [2]
			output.append (str (temp1 + "\"" + dev + "\"" + temp2))
		elif "test: " in line:
			temp1 = line.split ("\"") [0]
			temp2 = line.split ("\"") [2]
			output.append (str (temp1 + "\"" + test + "\"" + temp2))
		else:
			output.append (line)
	print (str (output))
	with open (jsonnet_file, 'w') as writing:
		writing.writelines (output)