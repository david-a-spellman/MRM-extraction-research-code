import json
import random

k = 3
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
random.shuffle (org_json_list)
random.shuffle (org_json_list)
random.shuffle (org_json_list)
folds = list ()
for x in range (0, k):
	folds.append (list ())
size = int (len (org_json_list) / 3) + 1
i = 0
for item in org_json_list:
	if i < size:
		folds [0].append (item)
	elif i < (2 * size):
		folds [1].append (item)
	else:
		folds [2].append (item)
	i += 1

# Print the lengths of each dataset
print (str (len (folds [0])))
print (str (len (folds [1])))
print (str (len (folds [2])))

fold1_string_list = list ()
for item in folds [0]:
	fold1_string_list.append (json.dumps (item) + "\n")

fold2_string_list = list ()
for item in folds [1]:
	fold2_string_list.append (json.dumps (item) + "\n")

fold3_string_list = list ()
for item in folds [2]:
	fold3_string_list.append (json.dumps (item) + "\n")

# Write to files
file_name = "C:\\data\\fold1_DIGGIE++_input_titles_3-fold_CV.json"
with open (file_name, 'w') as writing:
	writing.writelines (fold1_string_list)

file_name = "C:\\data\\fold2_DIGGIE++_input_titles_3-fold_CV.json"
with open (file_name, 'w') as writing:
	writing.writelines (fold2_string_list)

file_name = "C:\\data\\fold3_DIGGIE++_input_titles_3-fold_CV.json"
with open (file_name, 'w') as writing:
	writing.writelines (fold3_string_list)
print ("DONE!!!")