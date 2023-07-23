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
# Itterate over each title to find words to accumulate in a vocab list
# If a token is not in the vocab list it is added
vocabulary = list ()
for title in org_json_list:
	tokens = title ["sentences"] [0] [0]
	for token in tokens:
		if not token in vocabulary:
			vocabulary.append (token)
file_name = "C:\\data\\cancer_knowledge_vocabulary.json"
with open (file_name, 'w') as writing:
	json.dump (vocabulary, writing)
print ("DONE!!!")