from convert_to_scierc_format_functions import create_tokens
import csv
import json

# Purpose of this script is to take data that we want to perform event extraction on
# And get it into the format that Allen NLP can do predictions on
# Will be the same dictionary format as the training data but without the "events" key 

file_name = "/mnt/c/data/titles_with_two_verbs_and_gene_v3.csv"
json_list = list ()
with open (file_name, 'r') as file:
	read = csv.reader (file)
	#print (len (next (read)))
	#print (len (next (read)))
	for title in read:
		json_entry = dict ()
		json_entry ["doc_key"] = title [0]
		json_entry ["dataset"] = "1"
		#print (type (title [1]))
		#print (title [1])
		fix_punctuation = False
		if len (title [1].split (".")) > 2:
			#print ("PROBLEM!!!")
			actual_title = title [1].replace (".", "")
			fix_punctuation = True
		else:
			actual_title = title [1]
		tokenized_title = list ()
		split_title = actual_title.split (" ")
		for item in split_title:
			tokenized_segment = create_tokens (item)
			#print (tokenized_segment)
			for token in tokenized_segment:
				tokenized_title.append (token)
		if fix_punctuation:
			tokenized_title.append (".")
		#print (tokenized_title)
		json_entry ["sentences"] = list ()
		json_entry ["sentences"].append (tokenized_title)
		json_entry ["events"] = list ()
		json_entry ["events"].append (list ())
		json_entry ["events"] [0].append (list ())
		json_entry ["events"] [0] [0].append (list ())
		json_entry ["events"] [0] [0] [0].append (0)
		json_entry ["events"] [0] [0] [0].append ("regulation")
		json_list.append (json_entry)
# Write to output file
json_string_list = list ()
for item in json_list:
	json_string_list.append (json.dumps (item) + "\n")
file_name = "/mnt/c/data/knowledge_extraction_dataset2.json"
with open (file_name, 'w') as writing:
	writing.writelines (json_string_list)
print ("DONE!!!")