import json
from nltk.tokenize import word_tokenize as tokenize

# titles_with_two_verbs_and_gene_v3.csv
# unsupervised_titles_utf8.csv

def getTokenizedTitle (data, pmid):
	record = data [pmid]
	record = record.replace ("(", " ")
	record = record.replace (")", " ")
	record = record.replace ("[", " ")
	record = record.replace ("]", " ")
	tokenized = tokenize (record)
	return tokenized

# produce the final json entry for instance
def getJSONLine (title, pmid):
	result = dict ()
	result ["doc_key"] = pmid
	result ["dataset"] = "1"
	sentences = list ()
	sentences.append (title)
	result ["sentences"] = sentences
	#events = list ()
	#events.append (list ())
	#events [0].append (list ())
	#events [0] [0].append ([1, "regulation"])
	#events [0] [0].append ([0, 0, "initiator"])
	#events [0] [0].append ([2, 2, "process"])
	#events [0] [0].append ([3, 3, "location"])
	#events [0] [0].append ([4, 4, "target"])
	#result ["events"] = events
	result_string = json.dumps (result)
	return str (result_string + "\n")

fn2 = "C:\\data\\unsupervised_titles_utf8.csv"

titles = list ()
raw_titles = dict ()
with open (fn2, 'r', encoding = "utf8") as file:
	titles = file.readlines ()
print (len (titles))
for title in titles:
	raw_titles [title [0:8]] = title [9:-1].replace ("\n", "")
print (len (raw_titles))
data_instance_strings = list ()
title = ""
z = 0
for pmid in raw_titles:
	z += 1
	#print (z)
	title = getTokenizedTitle (raw_titles, pmid)
	json_string = getJSONLine (title, pmid)
	data_instance_strings.append (json_string)
print (len (data_instance_strings))
pred = data_instance_strings

file_name = "C:\\data\\prescreen_dataset_2.jsonl"
print (len (pred))
with open (file_name, 'w') as file:
	file.writelines (pred)
print ("DONE !!!")