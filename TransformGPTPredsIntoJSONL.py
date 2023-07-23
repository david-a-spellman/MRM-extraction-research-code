import json
from nltk.tokenize import word_tokenize as tokenize

# m6A_MRM_titles_4_args_test.csv
#  gpt3.5_incontext learning.csv
fn2 = ".\\gpt3.5_incontext learning.csv"
# Arg4FreeNewTriggerPunctuated.json

# output file
file_name = ".\\gpt3.5_incontext learning.jsonl"

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
def getLabels (annotation, title, pred):
	annotation = annotation.replace ("(", " ")
	annotation = annotation.replace (")", " ")
	annotation = annotation.replace ("[", " ")
	annotation = annotation.replace ("]", " ")
	if pred:
		content = annotation.split (",") [-5:]
	else:
		content = annotation.split (",") [-9:-4]
	print (content)
	labels = list ()
	mapping = {0 : "initiator", 1 : "process", 2 : "location", 3 : "target", 4 : "regulation"}
	for string in content:
		i = content.index (string)
		if (i >= 5) or (string == "") or (string == " "):
			continue
		tokens = tokenize (string)
		#print (string)
		#print (len (string))
		#print (tokens)
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
		#if (ec >= 2) or (sc >= 2):
			#print ("PROBLEM TITLE !!! PMID: " + pmid)
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
				if not (start in title):
					#print (title)
					#print (start)
					while len (start) >= 4:
						start = start [0:-2]
						for word in title:
							if (start in word) and (len (start) >= 4) and (start [0] == word [0]):
								result.append (title.index (word))
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
				if not (end in title):
					#print (end)
					#print (title)
					while len (end) >= 4:
						end = end [0:-2]
						for word in title:
							if (end in word) and (len (end) >= 4) and (end [0] == word [0]):
								result.append (title.index (word))
				else:
					result.append (title.index (end))
			result.append (mapping [i])
		else:
			if not (start in title):
				#print (title)
				#print (start)
				while len (start) >= 4:
					start = start [0:-2]
					for word in title:
						if (start in word) and (len (start) >= 4) and (start [0] == word [0]):
							result.append (title.index (word))
			else:
				result.append (title.index (start))
			result.append (mapping [i])
		#if (ec >= 2) or (sc >= 2):
			#print (result)
		labels.append (result)
	new_labels = list ()
	for i in range (1, len (labels) + 1):
		new_labels.append (labels [- i])
	labels = new_labels
	return labels

# produce the final json entry for instance
def getJSONLine (title, pmid, labels_true, labels_pred):
	result = dict ()
	result ["doc_key"] = pmid
	result ["dataset"] = "1"
	sentences = list ()
	sentences.append (title)
	result ["sentences"] = sentences
	events = list ()
	events.append (list ())
	events [0].append (labels_true)
	result ["events"] = events
	predicted_events = list ()
	predicted_events.append (list ())
	predicted_events [0].append (labels_pred)
	result ["predicted_events"] = predicted_events
	result_string = json.dumps (result)
	return str (result_string + "\n")

fn1 = "C:\\data\\m6A_MRM_titles_4_args_test.csv"
fn3 = "C:\\data\\Arg4FreeNewTriggerPunctuated.json"

pmids = list ()
use = list ()
actuals = list ()
with open (fn1, 'r') as file:
	pmids = file.readlines ()
pmids [0] = ""
new_pmids = list ()
for pmid in pmids:
	if len (pmid) > 5:
		#print (pmid)
		use.append (pmid [-4])
		actuals.append (pmid)
		new_pmids.append (pmid [0:9])
pmids = new_pmids
arguments = list ()
with open (fn2, 'r') as file:
	arguments = file.readlines ()
arguments [0] = ""
new_arguments = list ()
for argument in arguments:
	if len (argument) > 5:
		new_arguments.append (argument.replace ("\n", ""))
arguments = new_arguments
#print (use)
new_arguments = list ()
for i in range (0, len (pmids)):
	if use [i] == "1":
		new_arguments.append (str (pmids [i] + arguments [i]))
#print (new_arguments)
arguments = new_arguments
raw_titles = dict ()
with open (fn3, 'r') as file:
	string = file.read ()
	raw_titles = json.loads (string)
data_instance_strings = list ()
title = ""
z = 0
for pmid in raw_titles:
	z += 1
	#print (z)
	args = None
	acts = None
	for line in arguments:
		if pmid in line:
			args = line
	if args == None:
		continue
	for line in actuals:
		if pmid in line:
			acts = line
	if acts == None:
		continue
	#print (args [-4])
	title = getTokenizedTitle (raw_titles, pmid)
	new_title = list ()
	for token in title:
		new_title.append (token.lower ())
	title = new_title
	labels_pred = getLabels (args, title, True)
	if len (labels_pred) <= 1:
		continue
	for label in labels_pred:
		label.append (float (50))
		label.append (float (1))
	labels_true = getLabels (acts, title, False)
	if len (labels_true) <= 1:
		continue
	json_string = getJSONLine (title, pmid, labels_true, labels_pred)
	data_instance_strings.append (json_string)
test = data_instance_strings

print (len (test))
with open (file_name, 'w') as file:
	file.writelines (test)
print ("DONE !!!")