import json
from nltk.tokenize import word_tokenize as tokenize

# PM_labels_with_revised_triggers_and_no_argument4.csv
# Arg4FreeNewTriggerPunctuated.json

def getTokenizedTitle (data, pmid):
	record = data [pmid] ["document"]
	record = record.replace ("(", " ")
	record = record.replace (")", " ")
	record = record.replace ("[", " ")
	record = record.replace ("]", " ")
	tokenized = tokenize (record)
	return tokenized

# title is already tokenized is the assumption
# labels are tokenized and matched here
def getLabels (annotation, title):
	annotation = annotation.replace ("(", " ")
	annotation = annotation.replace (")", " ")
	annotation = annotation.replace ("[", " ")
	annotation = annotation.replace ("]", " ")
	content = annotation.split (",") [-9:-4]
	#print (content)
	labels = list ()
	mapping = {0 : "initiator", 1 : "process", 2 : "location", 3 : "target", 4 : "regulation"}
	for string in content:
		i = content.index (string)
		if (i >= 5) or string == "":
			continue
		tokens = tokenize (string)
		start = tokens [0].lower ()
		end = tokens [-1].lower ()
		result = list ()
		if not start in title:
			for token in title:
				if start in token:
					start = token
					break
		if not end in title:
			for token in title:
				if end in token:
					end = token
					break
		sc = 0
		ec = 0
		for token in title:
			if start == token:
				sc += 1
			if end == token:
				ec += 1
		if (ec >= 2) or (sc >= 2):
			print ("PROBLEM TITLE !!! PMID: " + pmid)
		#print (title)
		#print (start)
		#print (end)
		if i < 4:
			if (ec >= 2) and (sc >= 2):
				print (title)
				return []
			if sc >= 2:
				starts = list ()
				for i in range (0, len (title)):
					token = title [i]
					if token == start:
						starts.append (i)
				for i in range (0, len (starts)):
					if (i + 1) == len (starts):
						result.append (starts [i])
						break
					if (starts [i] < title.index (end)) and (starts [i + 1] > title.index (end)):
						result.append (starts [i])
						break
			else:
				result.append (title.index (start))
			if ec >= 2:
				ends = list ()
				for i in range (0, len (title)):
					token = title [i]
					if token == end:
						ends.append (i)
				for i in range (0, len (ends)):
					if ends [i] > title.index (start):
						result.append (ends [i])
						break
			else:
				result.append (title.index (end))
			result.append (mapping [i])
		else:
			result.append (title.index (start))
			result.append (mapping [i])
		if (ec >= 2) or (sc >= 2):
			print (result)
		labels.append (result)
	new_labels = list ()
	for i in range (1, len (labels) + 1):
		new_labels.append (labels [- i])
	labels = new_labels
	return labels

# produce the final json entry for instance
def getJSONLine (title, pmid, labels):
	result = dict ()
	result ["doc_key"] = pmid
	result ["dataset"] = "1"
	sentences = list ()
	sentences.append (title)
	result ["sentences"] = sentences
	events = list ()
	events.append (list ())
	events [0].append (labels)
	result ["events"] = events
	result_string = json.dumps (result)
	return str (result_string + "\n")

fn1 = "C:\\data\\PM_labels_with_revised_triggers_and_no_argument4.csv"
fn2 = "C:\\data\\Arg4FreeNewTriggerPunctuated.json"

arguments = list ()
with open (fn1, 'r') as file:
	arguments = file.readlines ()
for argument in arguments:
	argument.replace ("\n", "")
raw_titles = dict ()
with open (fn2, 'r') as file:
	string = file.read ()
	raw_titles = json.loads (string)
data_instance_strings = list ()
title = ""
z = 0
for pmid in raw_titles:
	z += 1
	#print (z)
	args = None
	for line in arguments:
		if pmid in line:
			args = line
	if args == None:
		continue
	#print (args [-4])
	use_instance = args [-3]
	if use_instance == '0':
		continue
	title = getTokenizedTitle (raw_titles, pmid)
	new_title = list ()
	for token in title:
		new_title.append (token.lower ())
	title = new_title
	labels = getLabels (args, title)
	if len (labels) <= 1:
		continue
	json_string = getJSONLine (title, pmid, labels)
	data_instance_strings.append (json_string)
train = list ()
test = list ()
dev = list ()
i = 0
for string in data_instance_strings:
	if i < 300:
		train.append (string)
	elif i < 380:
		dev.append (string)
	else:
		test.append (string)
	i += 1
file_name = "C:\\data\\train_4_args.jsonl"
print (len (train))
with open (file_name, 'w') as file:
	file.writelines (train)
file_name = "C:\\data\\dev_4_args.jsonl"
print (len (dev))
with open (file_name, 'w') as file:
	file.writelines (dev)
file_name = "C:\\data\\test_4_args.jsonl"
print (len (test))
with open (file_name, 'w') as file:
	file.writelines (test)
print ("DONE !!!")