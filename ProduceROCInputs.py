import json
import os
import numpy as np

# function to compute inverse logit to get prediction scores from logit prediction scores
def inverse_logit (value):
	return (1 / (1 + np.exp (- value)))

# final compiled list of successful titles
perfect_title_output_string_list = list ()
# final compiled list of titles with imperfect predictions
flawed_title_output_string_list = list ()

# Function for creating two files, a file with perfectly predicted titles and their summarized annotations, and a file with failed 
# titles where each failed title has a summary of what differed between the actual and predicted
def compile_specifics_of_results (pm_id, sentence, class_title_lists):
	match = True
	for key in class_title_lists:
		for item in class_title_lists [key]:
			if item [0] != item [1]:
				match = False
	if match:
		out_str = str (pm_id + "\n" + str (sentence) + "\n")
		for key in class_title_lists:
			out_str += key
			out_str += ": "
			for i in range (0, len (class_title_lists [key])):
				if class_title_lists [key] [i] [0] == 1:
					out_str += sentence [i]
					out_str += " "
			out_str += "\n"
		perfect_title_output_string_list.append (out_str)
	# Case where the prediction has issues
	else:
		out_str = str (pm_id + "\n" + str (sentence) + "\n")
		# Do not bother adding the trigger/argument to the output if it was predicted correctly
		for key in class_title_lists:
			match = True
			for item in class_title_lists [key]:
				if item [0] != item [1]:
					match = False
			if match:
				continue
			# If trigger / argument not predicted correctly print both actual and predicted versions
			else:
				out_str += "actual "
				out_str += key
				out_str += ": "
				for i in range (0, len (class_title_lists [key])):
					if class_title_lists [key] [i] [0] == 1:
						out_str += sentence [i]
						out_str += " "
				out_str += "\n"
				out_str += "predicted "
				out_str += key
				out_str += ": "
				for i in range (0, len (class_title_lists [key])):
					if class_title_lists [key] [i] [1] == 1:
						out_str += sentence [i]
						out_str += " "
				out_str += "\n"
		flawed_title_output_string_list.append (out_str)

# dictionary for capturing the mapping from output dictionary keys to the original prediction dictionary keys
argument_type_dict = {"argument1_initiator": "initiator", "argument2_process": "process", "argument3_location": "location", "argument4_mechanism": "mechanism", "argument5_target": "target"}

# Method to produce a single tuple by first branching on the key for the trigger / event type
# Then produces the tuple to be returned by itterating over the ground truth lists and the prediction lists
def produce_binary_tuples (key, index, gt, pred):
	actual = 0
	predicted = 0
	probability = "none"
	# Case for the trigger since the trigger annotations and predictions are structured a bit differently than the arguments
	if key == "trigger_regulation":
		for item in gt:
			if "regulation" in item:
				actual_index = item [0]
				if index == actual_index:
					actual = 1
		for item in pred:
			if "regulation" in item:
				predicted_index = item [0]
				if index == predicted_index:
					predicted = 1
					probability = inverse_logit (float (item [-2]))
		return (actual, predicted, probability)
	# Cases that cover the arguments
	else:
		argument_type = argument_type_dict [key]
		for item in gt:
			if argument_type in item:
				actual_index_start = item [0]
				actual_index_end = item [1]
				if index >= actual_index_start and index <= actual_index_end:
					actual = 1
		for item in pred:
			if argument_type in item:
				predicted_index_start = item [0]
				predicted_index_end = item [1]
				if index >= predicted_index_start and index <= predicted_index_end:
					predicted = 1
					probability = inverse_logit (float (item [-2]))
		return (actual, predicted, probability)

# function to compile the trig list and arg lists for a single predictions file
# Will take a list of prediction dictionaries as input
# Will output a dictionary with the trigger type and argument types as keys, and a list of tuples as the value for each key
# All lists in this output dictionary should be the same length
# Each tuple corresponds to a token in a title
# index 0  of a tuple is actual class, index 1 is predicted class
# Each token in the sentence has an entry so that the data can be encoded in binary so that it can be input to the sklearn functions for ROC and AUC

def get_arg_and_trig_lists (org_json_list):
	keys = ["trigger_regulation", "argument1_initiator", "argument2_process", "argument3_location", "argument4_mechanism", "argument5_target"]
	# dictionary holding all of the ground truths and predictions
	class_lists = dict ()
	for key in keys:
		class_lists [key] = list ()
	# Itterate over the titles
	for oj in org_json_list:
		# dictionary holding the title level ground truths and predictions that will be fed into the compilation function for exploratory result output
		class_title_lists = dict ()
		for key in keys:
			class_title_lists [key] = list ()
		# list of tokens in the titles as their string forms
		sentence = oj ["sentences"] [0]
		# The actual predictions as a list of lists with the token positions coming first in each of the nested lists
		gt = oj ["events"] [0] [0]
		# The predicted values as the same structure of the actual values but with two extra numbers at the end of each nested list
		if len (oj ["predicted_events"] [0]) == 0:
			#print (str (oj))
			pred = list ()
		else:
			pred = oj ["predicted_events"] [0] [0]
		# Itterate over the tokens in each sentence
		for token in sentence:
			# Itterate over trigger and argument types
			for key in keys:
				# Get the index of a single token to pass into the function call for determining a single tuple
				index = sentence.index (token)
				# Function that produces a single tuple
				result = produce_binary_tuples (key, index, gt, pred)
				if result [1] == 1 and result [-1] != "none":
					temp = (result [0], result [-1])
					class_lists [key].append (temp)
				class_title_lists [key].append (result)
		# Now invoke the specific example compilation function before moving onto next testing title
		pm_id = oj ["doc_key"]
		compile_specifics_of_results (pm_id, sentence, class_title_lists)
	return class_lists

# Method to itterate over a list of prediction files for a k fold cross validation and create input lists for calculating ROC and AUC with sklearn
# For each input file six output files are created as lists dumped to file using the json library
# For each file the trigger and five arguments are itterated over to make a list of  binary tuples with the first element of the tuple being actual and the second being predicted
# For each trigger and argument there will be a tuple for each token in the sentence
# So each trigger or argument combined with a token will have an entry in this list for calculating TPR and FPR
# This is necessary since sklearn only takes binary inputs for calculating ROC and AUC

def create_ROC_AUC_input_lists (file_list, output_directory):
	result_files = list ()
	if not os.path.isdir (output_directory):
		os.mkdir (output_directory)
	for file_name in file_list:
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
		output_files = get_arg_and_trig_lists (org_json_list)
		for key in output_files:
			org_name = file_name.split ("\\") [-1].split (".") [0]
			number = ""
			for j in range (0, len (org_name)):
				if org_name [j].isnumeric ():
					number += org_name [j]
			#print (str (key))
			#print (str (number))
			if len (number) > 1:
				number = number [-1]
			output_file_name = str (output_directory + key + "_fold_" + number + "_ROC_input_list.json")
			result_files.append (output_file_name)
			with open (output_file_name, 'w') as writing:
				json.dump (output_files [key], writing)
			#print (output_file_name)
			#print (str (len (output_files [key])))
	write_compiled_result_lists (output_directory)
	return result_files

def write_compiled_result_lists (output_directory):
	file_name = str (output_directory + "perfect_title_output_string_list3.txt")
	with open (file_name, 'w') as writing:
		writing.writelines (perfect_title_output_string_list)
	file_name = str (output_directory + "flawed_title_output_string_list3.txt")
	with open (file_name, 'w') as writing:
		writing.writelines (flawed_title_output_string_list)

# function for loading in all json
def getPredictionDicts (file):
	# Load file
	json_list = list ()
	strings = list ()
	with open (file, 'r') as f:
		strings = f.readlines ()
	json_strings = list ()
	# Clean up strings
	for string in strings:
		json_strings.append (string.replace ("\n", ""))
	# Append to json_list
	for string in json_strings:
		json_list.append (json.loads (string))
	return json_list

# Function to apply correction to each argument
def getBestPred (arg):
	if len (arg) == 0:
		return None
	elif len (arg) == 1:
		return arg [0]
	best_index = 0
	for i in range (0, len (arg)):
		current = arg [i]
		if current [-2] > arg [best_index] [-2]:
			best_index = i
	return arg [best_index]

# Itterate over argument predictions for individual title dictionary and return a cleaned up copy without redundant argument classifications
def getCleanedPredictions (title):
	new_title = title
	# Itterate over predictions for title
	a1 = list ()
	a2 = list ()
	a3 = list ()
	a5 = list ()
	t = list ()
	if len (title ["predicted_events"] [0]) == 0:
		return title
	for pred in title ["predicted_events"] [0] [0]:
		if "regulation" in pred:
			t.append (pred)
		elif "initiator" in pred:
			a1.append (pred)
		elif "process" in pred:
			a2.append (pred)
		elif "location" in pred:
			a3.append (pred)
		elif "target" in pred:
			a5.append (pred)
	# Populate new predictions list
	new_preds = list ()
	new_preds.append (list ())
	new_preds [0].append (list ())
	a1 = getBestPred (a1)
	a2 = getBestPred (a2)
	a3 = getBestPred (a3)
	a5 = getBestPred (a5)
	t = getBestPred (t)
	if a1 != None:
		new_preds [0] [0].append (a1)
	if a2 != None:
		new_preds [0] [0].append (a2)
	if a3 != None:
		new_preds [0] [0].append (a3)
	if a5 != None:
		new_preds [0] [0].append (a5)
	if t != None:
		new_preds [0] [0].append (t)
	new_title ["predicted_events"] = new_preds
	return new_title

# function to eliminate redundant argument predictions
# Only take the classified argument span with the highest output logit score, and throw away the rest
# Write out to file a cleaned up version of the predictions
# Returns the new files
def cleanUpPredictions (files):
	# Loop over all files
	new_files = list ()
	for file in files:
		json_list = getPredictionDicts (file)
		new_json_list = list ()
		# Itterate over each predicted title
		for title in json_list:
			new_json_list.append (getCleanedPredictions (title))
		json_output = list ()
		for item in new_json_list:
			json_output.append (str (json.dumps (item) + "\n"))
		file_split = file.split (".")
		new_file = str (file_split [0] + "_cleaned." + file_split [1])
		new_files.append (new_file)
		with open (new_file, 'w') as writing:
			writing.writelines (json_output)
	return new_files

# EOF