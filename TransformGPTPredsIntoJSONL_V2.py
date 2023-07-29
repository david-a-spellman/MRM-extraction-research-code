import json
from nltk.tokenize import word_tokenize as tokenize

# july_18_test_samples_V3.tsv
#  pred_results_prompt_1_0.csv
fn2 = ".\\pred_results_prompt_1_0.csv"
# Arg4FreeNewTriggerPunctuated.json

# output file
file_name = str ("." + fn2.split (".") [1] + ".jsonl")

# Helper function for replacing tabs with "*&^&*"
def replaceTabs (string):
	# Have to replace "\t" the hard way
	temp = ""
	j = 0
	while j < len (string):
		c = string [j]
		#if (j + 1) < len (string):
		#	c2 = string [j + 1]
		#else:
		#	c2 = ""
		#if (c1 == "\\") and (c2 == "t"):
		if c == "\t":
			temp += "*&^&*"
			j += 1
		else:
			temp += c
			j += 1
	return temp

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
	#print (annotation)
	annotation = annotation.replace ("(", " ")
	annotation = annotation.replace (")", " ")
	annotation = annotation.replace ("[", " ")
	annotation = annotation.replace ("]", " ")
	# Handeling case with different format for predictions from Chat GPT
	if pred:
		content = annotation.split ("*&^&*") [-5:]
	# Case for the gold labels, or target annotations
	else:
		content = annotation.split ("*&^&*") [-9:-4]
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

fn1 = "C:\\data\\july_18_test_samples_V3.tsv"
fn3 = "C:\\data\\Arg4FreeNewTriggerPunctuated.json"

# Temperary list for collecting the target titles
titles = list ()
# List for collecting flags telling whether to use a title for evaluation or not
use = list ()
# List where targets will be processed from
actuals = list ()
with open (fn1, 'r') as file:
	titles = file.readlines ()
titles [0] = ""
# List for matching up the titles for targets and predictions
check_titles = list ()
for title in titles:
	# Don't use item if not a full sample, checking for extra newlines or other junk
	if len (title) > 5:
		#print (title)
		# Use flag should be 0 for do not use, or 1 for good
		#print (title [-4])
		use.append (title [-4])
		# List to pass in as the targets
		actuals.append (title)
		# Will be used in substring check comparison
		temp = replaceTabs (title)
		check_titles.append (temp.split ("*&^&*") [1])
# Recycling variable
titles = check_titles
# Getting the predictions
predictions = list ()
with open (fn2, 'r') as file:
	predictions = file.readlines ()
predictions [0] = ""
# Temp list to process predictions
new_predictions = list ()
for pred in predictions:
	if len (pred) > 5:
		temp = pred.replace ("\n", "")
		new_predictions.append (temp)
# Recycle variables
predictions = new_predictions
#print (titles [0])
#print (predictions [0])
# List for predictions ready to be processed
new_predictions = list ()
# List of targets ready to be processed, and sorted by matching index to new_predictions list
checked_targets = list ()
# The same list but just with the title field
checked_titles = list ()
for i in range (0, len (predictions)):
	pred = predictions [i]
	for j in range (0, len (titles)):
		title = titles [j]
		# check that target and prediction are for the same title using the full title
		if title in pred:
			# Prediction and target are for the same title
			print (str (i) + " matches!")
			# Now check to see that this title should be evaluated
			if use [j] == "1":
				# They match and should be evaluated
				print (str (i) + " is good!")
				# Now check to see if the original title contained commas
				temp = ""
				if "," in title:
					# Title has commas, so take the predictions input and convert all delimiter commas to "*&^&*" as a new delimiter
					# When having just counted an odd number of quotes, we will know that all commas in that part of the string are valid non-delimiter commas
					# variable for counting the quotes
					count = 0
					# itterate over the characters in the prediction string
					for c in pred:
						# Case where we have hit a quote to count
						if c == "\"":
							count += 1
						# Case where we have hit a comma
						elif c == ",":
							# Even count case where comma is replaced with "*&^&*"
							if (count % 2) == 0:
								temp += "*&^&*"
							# Odd case where we keep the comma the same as it is part of the data
							else:
								temp += ","
						# Case where we hit another character that just gets appended
						else:
							temp += c
				# Case where the title has no commas, so all commas are delimiters that can be replaced
				else:
					temp = pred.replace (",", "*&^&*")
				# Append this new prediction string with cleaned up delimiters
				new_predictions.append (str (actuals [j] [0:8] + "*&^&*" + temp))
				# Append the valid title
				checked_titles.append (title)
				# Append the valid targets
				temp = replaceTabs (actuals [j])
				checked_targets.append (temp)
			break
#print (new_predictions)
#print (checked_targets)
predictions = new_predictions
# Get previously tokenized versions of punctuated titles and labels
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
	# Variable holding the prediction for the particular title
	args = None
	# Variable holding the labels for the particular title
	acts = None
	# Iterating over the valid predictions
	for line in predictions:
		if pmid in line:
			args = line
	if args == None:
		continue
	for line in checked_targets:
		if pmid in line:
			acts = line
	if acts == None:
		continue
	title = getTokenizedTitle (raw_titles, pmid)
	new_title = list ()
	for token in title:
		new_title.append (token.lower ())
	title = new_title
	# Call to get the predicted classifications
	labels_pred = getLabels (args, title, True)
	if len (labels_pred) <= 1:
		continue
	for label in labels_pred:
		label.append (float (50))
		label.append (float (1))
	# Getting the ground truth labels
	labels_true = getLabels (acts, title, False)
	if len (labels_true) <= 1:
		continue
	# Function to get a single line of the JSON
	json_string = getJSONLine (title, pmid, labels_true, labels_pred)
	data_instance_strings.append (json_string)
test = data_instance_strings

# Now writing JSONL file out 
print (len (test))
with open (file_name, 'w') as file:
	file.writelines (test)
print ("DONE !!!")