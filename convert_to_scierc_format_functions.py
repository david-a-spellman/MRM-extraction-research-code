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
		return "mechanism"
	if arg == "arg5":
		return "target"

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