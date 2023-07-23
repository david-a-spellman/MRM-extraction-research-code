import json

"""
This file will convert a single json object of all data points into indevidual json objects for each data point.
Each data point will be on a single line as an indevidual json object.
"doc_key" will be the key for the PMID of a data point.
"dataset" Is the key to the value that marks what dataset the title belongs to, which is not important here but is required for training with this code.
"sentences" The key to the actual text data which must be in a tokenized form. This means a list of strings where each string is a token.
In data with multiple sentences this should be a list of lists where each nested list contains the tokens to an individual sentence. 
Even though we have only a single sentence per title the nested lists still need to be there.
The data cannot contain empty string in the sentence lists.
"weight" Is a float to multiply the loss of the title by during training if we want to acount for certain titles being better labeled than others so that the better labeled titles have a larger effect during training. 
"ner" Is the key to the named entities in the title. The ner value should be a list of sentence lists containing lists for the start and end tokens of each entity span in the sentence. 
"relations" The key to the list structure of relations to be extracted. Once again it should be a list of sentence lists containing lists for each relation in that sentence. 
Each relation list within a sentence list should contain the start and end tokens of each span in the relation followed by the token that describes the relation. Words in a relation token should be seperated by a '-'. 
"clusters" This is for coereference clusters which for our titles will be empty but this still must be included but will not be used in our training configuration.
If there were any coreferences the list would contain the coreference lists which themselves would contain span lists with the start and end tokens for one of the spans falling into that coreference. 
"events" Key for the events we want extracted. The value should be a list of sentence lists where each sentence list contains event lists where each event list contains a trigger list, and a list for each argument in the template.
The trigger list should have the single token position followed by the trigger token, and each argument list should contain the start and end tokens of the argument followed by the argument string, or string that describes the role of the labeled argument.
For example, [0, 1, "mechanism"] not [0, 1, "m6A methylation"]
"event_clusters" Key to coreferences for events. Once again this is not necessary for us since we are using one template. This value should be a list of coreferenced event list where each entry is a list containing the start and end token of the coreferenced event's trigger word.
"""

# function for checking correctness of tokenization
def check_tokenization (t, s):
	comp = ""
	for k in range (0, len (t)):
		if k == (len (t) - 1):
			comp += t [k]
		elif t [k] != "." and t [k + 1] != "," and t [k + 1] != ";" and t [k + 1] != ":":
			comp += t [k]
			comp += " "
		else:
			comp += t [k]
	if comp == s:
		return True
	else:
		return False

# function for fixing problematic labels because they do not match the text in the title
# This allows for quick fixes through the commandline
def fix_label (id, arg, title, new_org_json):
	org_label = new_org_json [id] ["annotation"] [0] [arg]
	if ' ' in org_label:
		org_label = org_label.split(' ')[0]
	invalid = True
	suggestion = -1
	for i in range (0, len (title)):
		if org_label in title [i]:
			suggestion = i
	print ("suggested word: " + title [suggestion] + " starting index of suggested word: " + str (suggestion))
	while invalid:
		start = int (input ("Enter the indicies of the tokens belonging in the valid label for this argument. Indexes 0 to " + str (len (title) - 1) + " are possible and the range of indicies entered must be given one at a time with the first index first and the last index last. FIRST INDEX: "))
		if start < 0 or start >= len (title):
			continue
		end = int (input ("LAST INDEX: "))
		if end < 0 or end >= len (title):
			continue
		invalid = False
	label = ""
	for i in range (start, end + 1):
		if label != "" or title [i] != "." or title [i] != "," or title [i] != ";" or title [i] != ":":
			label += " "
		label += title [i]
	if label [0] == " ":
		label = label [1: len (label)]
	answer = input (str ("Is " + label + " correct? (1 to confirm / any other input to cancel): "))
	if answer != "1":
		return fix_label (id, arg, title, new_org_json)
	#print (arg)
	new_org_json [id] ["annotation"] [0] [arg] = label
	named_entity = list ()
	named_entity.append (start)
	named_entity.append (end)
	named_entity.append (type_entity (arg))
	return new_org_json, named_entity

# Simple function for roughly distinguishing RNAs, proteins, genes, and molecules
"""
def gene_rna_protein_molecule (arg, label):
	if "rna" in tolower (label):
		return "RNA"
	if "protein" in tolower (label):
		return "protein"
	if label.isalpha ():
		return "molecule"
	temp = ""
	no_numbers = True
	for c in label:
		if not c.isnumeric () and no_numbers:
			temp += c
		elif no_numbers:
			no_numbers = False
		elif not c.isnumeric ():
			return "mechanism"
	return "gene"
"""

# Simple function for producing rough data for NER
# We are not intrested in NER but this data is still required for training
def type_entity (arg):
	#print (str ("entity: " + label))
	"""
	if arg == "arg1":
		return gene_rna_protein_molecule (arg, label)
	if arg == "arg2":
		return "process"
	if arg == "arg3":
		if "cell" in tolower (label):
			return "cell"
		else:
			return "disease"
	if arg == "arg4" or arg == "arg5":
		if ("-" in label and not ("mi-" in tolower (label) or "rna" in tolower (label))) or "pathway" in tolower (label) or "signal" in tolower (label) or label.isalpha () or "m6a" in tolower (label) or "methylation" in tolower (label):
			return "mechanism"
		else:
			return gene_rna_protein_molecule (arg, label)
	"""
	if arg == "arg1":
		return "initiator"
	if arg == "arg2":
		return "process"
	if arg == "arg3":
		return "location"
	if arg == "arg4":
		return "target"
	if arg == "arg5":
		print ("ARGUMENT ISSUE!!! Exiting program")
		quit ()

def create_tokens (segment):
	tokenized_segment = list ()
	#print (title)
	"""if "|" in segment or "+" in segment or "\\" in segment or "?" in segment or "!" in segment:
		print (segment)"""
	if " " in segment:
		print ("ISSUE!")
		quit ()
	elif "," in segment:
		tokenized_segment.append (segment.replace (",", ""))
		tokenized_segment.append (",")
	elif "." in segment:
		if segment [-1] == ".":
			tokenized_segment.append (segment.replace (".", ""))
			tokenized_segment.append (".")
		else:
			tokenized_segment.append (segment)
	elif ";" in segment:
		tokenized_segment.append (segment.replace (";", ""))
		tokenized_segment.append (";")
	elif ":" in segment:
		tokenized_segment.append (segment.replace (":", ""))
		tokenized_segment.append (":")
	else:
		tokenized_segment.append (segment)
	"""if "|" in segment or "+" in segment or "\\" in segment or "?" in segment or "!" in segment:
		print (str (tokenized_segment))"""
	return tokenized_segment

file_name = "C:\\data\\Cleaned_sciERC_input_no_arg4.json"
org_json = dict ()
with open (file_name, 'r') as reading:
	org_json = json.load (reading)
# Check org_json for issues
temp_json = org_json
for id in temp_json:
	labels = temp_json [id] ["annotation"] [0]
	for arg in labels:
		argument = labels [arg]
		if type (argument) != type (str ()):
			org_json [id] ["annotation"] [0] [arg] = argument [0]
# List of dictionaries for final processed sciERC input data
new_json_list = list ()
# Dictionary for writing back fixes to original cleaned json before preprocessing step
new_org_json = dict (org_json)
# boolean to track whether updates for fixes have been made to the original json
updates = False
# variable to track how many data points the script has progressed through
z = 0
event_types = ["initiator", "process", "location", "mechanism", "target"]
# Construct The lists for the tokenized titles as well as the ner lists with start and end token positions
for id in org_json:
	#print (type (org_json [id]))
	#print (id)
	title = org_json [id] ["document"]
	labels = org_json [id] ["annotation"] [0]
	#print (str (labels))
	new_json = dict ()
	tokenized_title = list ()
	ner = list ()
	#print (str (id + ": " + title))
	#print (title)
	labels = org_json [id] ["annotation"] [0]
	ner.append (list ())
	split_title = title.split (" ")
	for item in split_title:
		tokenized_segment = create_tokens (item)
		#print (tokenized_segment)
		for token in tokenized_segment:
			tokenized_title.append (token)
	#print (tokenized_title)
	tokenized_labels = dict ()
	for arg in labels:
		label = labels [arg]
		if label == "":
			tokenized_labels [arg] = list ()
			continue
		if label [0] == " ":
			label = label [1: len (label)]
			new_org_json [id] ["annotation"] [0] [arg] = label
			updates = True
		#print (label)
		split_label = label.split (" ")
		tokenized_label = list ()
		for item in split_label:
			tokenized_segment = create_tokens (item)
			#print (tokenized_segment)
			for token in tokenized_segment:
				tokenized_label.append (token)
		#print (tokenized_label)
		if check_tokenization (tokenized_label, label):
			tokenized_labels [arg] = tokenized_label

	# Now for adding in token positions for NER and event extraction by comparing the tokenized titles to tokenized labels
	#print (str (tokenized_title))
	for arg in tokenized_labels:
		tokens = tokenized_labels [arg]
		#print (str (tokens))
		if len (tokens) == 0:
			continue
		match = False
		match_all = False
		start = -1
		end = -1
		named_entity = None
		for item in tokenized_title:
			if item == tokens [0]:
				match = True
			if match:
				i = tokenized_title.index (item)
				match_all = True
				if (len (tokenized_title) - (i + 1)) < len (tokens):
					print (z)
					print ("ISSUE!")
					print (id)
					print (len (tokens))
					print (i)
					print (len (tokenized_title))
					print (tokenized_title [i])
					print (str (tokenized_title))
					print (str (tokens))
					new_org_json, named_entity = fix_label (id, arg, tokenized_title, new_org_json)
					print (str (named_entity))
					updates = True
					break
				for j in range (0, len (tokens)):
					if tokens [j] != tokenized_title [i]:
						match_all = False
					i += 1
			if match_all:
				if len (tokens) == 1:
					start = tokenized_title.index (tokens [0])
					end = tokenized_title.index (tokens [0])
				else:
					start = tokenized_title.index (tokens [0])
					end = tokenized_title.index (tokens [-1])
				break
		if named_entity != None:
			if tokens == tokenized_title [named_entity [0]: named_entity [1] + 1]:
				ner [0].append (named_entity)			
		elif start != -1 and end != -1:
			classification = type_entity (arg)
			"""if "and" in tokens:
				j = 0
				for token in tokens:
					if j > tokens.index (token):
						continue
					token2 = None
					if start < end:
						token2 = tokens [j + 1]
					else:
						token2 = ","
					if token != "," and token != "and" and token2 != "," and token2 != "and":
						temp_end = start
						temp = tokens [j + 1]
						while temp != "," and temp != "and":
							temp_end += 1
							j += 1
							if (j + 1) < len (tokens):
								temp = tokens [j + 1]
							else:
								break
						named_entity = list ()
						named_entity.append (start)
						named_entity.append (temp_end)
						named_entity.append (classification)
						if tokens == tokenized_title [named_entity [0]: named_entity [1] + 1]:
							ner [0].append (named_entity)
						#print (str (tokenized_title [start:temp_end + 1]))
						#print (str (named_entity))
						start = (temp_end + 1)
						j += 1
					elif token != "," and token != "and":
						named_entity = list ()
						named_entity.append (start)
						named_entity.append (start)
						named_entity.append (classification)
						if tokens == tokenized_title [named_entity [0]: named_entity [1] + 1]:
							ner [0].append (named_entity)
						#print (str (token))
						#print (str (named_entity))
						start += 1
						j += 1
					else:
						start += 1
						j += 1"""
			named_entity = list ()
			named_entity.append (start)
			named_entity.append (end)
			named_entity.append (classification)
			if tokens == tokenized_title [named_entity [0]: named_entity [1] + 1]:
				ner [0].append (named_entity)
			#print (str (tokens))
			#print (str (named_entity))
		else:
			print (z)
			print ("ISSUE!: label does not match title!")
			print (id)
			print (str (tokenized_title))
			print (str (tokens))
			new_org_json, named_entity = fix_label (id, arg, tokenized_title, new_org_json)
			if tokens == tokenized_title [named_entity [0]: named_entity [1] + 1]:
				ner [0].append (named_entity)
			updates = True
			print (str (named_entity))

	# Now using tokenized titles and labels to put together event data
	events = list ()
	events.append (list ())
	events [0].append (list ())
	events [0] [0].append (list ())
	trigger = org_json [id] ["trigger"]
	trigger_token = org_json [id] ["trigger"].split (" ") [0]
	# make sure that the actual trigger word is identified
	# we do not want words such as is, by, through, or via as the trigger
	# If the first word is a valid regulation verb then that word will be identified as the trigger
	if " " in trigger and (trigger_token == "is" or trigger_token == "by" or trigger_token == "via" or trigger_token == "through"):
		#print (str (z))
		#print (id)
		#print (trigger)
		trigger_token = trigger.split (" ") [1]
		if trigger_token == "is" or trigger_token == "by" or trigger_token == "via" or trigger_token == "through":
			print (trigger_token)
			print ("not fixed")
			quit ()
	# here we are double checking the triggers for the titles
	# If there is no real described event in title we can throw the title out after second thoughts
	# Titles without proper triggers are no good for training
	# If the trigger just needs fixed up we can do that here too
	throw_out = False
	if not trigger_token in tokenized_title:
		print ("TRIGGER ISSUE!: " + trigger_token + " not in title \n" + str (tokenized_title) + "\n" + "Select an alternative trigger token!")
		invalid = True
		while invalid:
			position = int (input ("Enter the index of the token belonging in the valid label for this trigger. Indexes 0 to " + str (len (tokenized_title) - 1) + " are possible. If the title should actually just be thrown out enter -1 to do so. INDEX: "))
			if position < -1 or position >= len (tokenized_title):
				continue
			if position == -1:
				throw_out = True
				break
			trigger_label = tokenized_title [position]
			answer = input (str ("Is " + trigger_label + " correct? (1 to confirm / any other input to cancel): "))
			if answer == "1":
				invalid = False
		if not throw_out:
			new_org_json [id] ["trigger"] = trigger_label
			updates = True
			trigger_token_index = position
	else:
		trigger_token_index = tokenized_title.index (trigger_token)
	if throw_out:
		print ("Throwing out title: " + id + "!!!" + "\n" + "Should not show up in output dataset")
		continue
	events [0] [0] [0].append (trigger_token_index)
	events [0] [0] [0].append ("regulation")
	j = 0
	for i in range (0, len (event_types)):
		t = event_types [i]
		if ner [0] [j] [2] == t:
			events [0] [0].append (ner [0] [j])
			j += 1
			if j == len (ner [0]):
				break
		else:
			#events [0] [0].append (list ())
			continue

	#print (str ("tokenized " + ": " + str (tokenized_title)))
	new_json ["doc_key"] = id
	new_json ["dataset"] = "1"
	new_json ["sentences"] = list ()
	new_json ["sentences"].append (tokenized_title)
	l_count = 0
	tl_count = 0
	for arg in tokenized_labels:
		if len (tokenized_labels [arg]) > 0:
			tl_count += 1
	for arg in labels:
		if labels [arg] != "":
			l_count += 1
	if l_count != tl_count:
		print (str (len (ner [0])))
		print (id)
		print (str (tokenized_title))
		i = 0
		for arg in labels:
			print (arg)
			print (labels [arg])
			if arg in tokenized_labels:
				print (str (tokenized_labels [arg]))
			else:
				print (arg + "is missing")
			print (str (ner [0] [i]))
			if i < (len (ner [0]) - 1):
				i += 1
	#new_json ["ner"] = ner
	new_json ["events"] = events
	new_json_list.append (new_json)
	if len (ner [0]) > 5:
		print (str (z))
		print (id + ":")
		print ("count: " + str (len (ner [0])))
		for item in ner [0]:
			print (str (item))
	z += 1
	if updates:
		file_name = "C:\\data\\Cleaned_sciERC_starting_dict.json"
		with open (file_name, 'w') as writing:
			json.dump (new_org_json, writing)
		updates = False
		print ("Wrote corrections back to original json file.")
#print (str (new_json_list))

# Write to output file
json_string_list = list ()
for item in new_json_list:
	json_string_list.append (json.dumps (item) + "\n")
file_name = "C:\\data\\DIGGIE++_arg4_free_input_titles.json"
with open (file_name, 'w') as writing:
	writing.writelines (json_string_list)
print ("DONE!!!")