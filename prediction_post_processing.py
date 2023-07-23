# Script for improving predictions using post processing after model makes initial predictions
from PostProcessingMethods import *
import json

arguments = ["initiator", "process", "location", "target"]
new_json_list = list ()
file_list = ["C:\\data\\no_arg4\\5-fold_predictions\\fold_1_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_2_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_3_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_4_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_5_predictions.jsonl"]
# Retrieving valid trigger words
verbs = readRegulationVerbs ("C:\\data\\regulation_verbs.csv")
# Reading in json for up-to-date annotations
file_name = "C:\\Users\\David\\Projects\\Title-Based-Molecular-Regulation-Event-Extraction\\data\\DIGGIE++_arg4_free_input_titles.json"
json_strings = list ()
updated_annotation_json_list = list ()
with open (file_name, 'r') as reading:
	json_strings = reading.readlines ()
for string in json_strings:
	if "\n" in string:
		#print ("contains endline character")
		new_string = string.replace ("\n", "")
		#print (string)
		updated_annotation_json_list.append (json.loads (new_string))
		continue
	#print (string)
	updated_annotation_json_list.append (json.loads (string))
#print (str (updated_annotation_json_list))
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
	#print (str (org_json_list))
	for title in org_json_list:
		# dictionary for tracking the scores of the predictions for each argument
		argument_scores = dict ()
		new_title = title
		token_list = list ()
		arg_dict = dict ()
		new_arg_dict = dict ()
		act_arg_dict = dict ()
		output = False
		if len (title ["predicted_events"] [0]) > 0:
			pred_trigger = title ["predicted_events"] [0] [0] [0]
			argument_scores ["trigger"] = (title ["predicted_events"] [0] [0] [0] [-2], title ["predicted_events"] [0] [0] [0] [-1])
		else:
			continue
		actual_trigger = title ["events"] [0] [0] [0]
		index_pred = pred_trigger [0]
		arg_dict ["trigger"] = index_pred
		index_actual = actual_trigger [0]
		act_arg_dict ["trigger"] = index_actual
		for token in title ["sentences"] [0]:
			token_list.append (token.lower ())
		# Code looping over argument predictions and invoking functions
		for argument in arguments:
			pred_arguments = title ["predicted_events"] [0] [0]
			pred_argument = None
			score = 0
			for i in range (0, len (pred_arguments)):
				if argument in pred_arguments [i]:
					if pred_argument != None and float (score) < float (pred_arguments [i] [-1]):
						if argument == "process":
							print ("hit: " + str (pred_arguments [i]) + "\t" + str (score))
						score = float (pred_arguments [i] [-1])
						pred_argument = pred_arguments [i]
						argument_scores [pred_argument [2]] = (pred_argument [-2], pred_argument [-1])
					elif pred_argument == None:
						if argument == "process":
							print ("hit: " + str (pred_arguments [i]) + "\t" + str (score))
						pred_argument = pred_arguments [i]
						argument_scores [pred_argument [2]] = (pred_argument [-2], pred_argument [-1])
						score = float (pred_argument [-1])
			# get the actual for each argument to help control output for debugging
			actual_arguments = title ["events"] [0] [0]
			actual_argument = None
			for i in range (0, len (actual_arguments)):
				if argument in actual_arguments [i]:
					actual_argument = actual_arguments [i]
			if pred_argument != None:
				if type (pred_argument [0]) == type (list ()):
					arg_dict [pred_argument [0] [2]] = list ()
					for item in pred_argument:
						index_pred = (item [0], item [1])
						arg_dict [item [2]].append ([item [0], item [1]])
				else:
					index_pred = (pred_argument [0], pred_argument [1])
					arg_dict [pred_argument [2]] = [pred_argument [0], pred_argument [1]]
			if actual_argument != None:
				index_actual = (actual_argument [0], actual_argument [1])
				act_arg_dict [actual_argument [2]] = [actual_argument [0], actual_argument [1]]
				"""if argument == "location":
					print (str (act_arg_dict))"""
			# logic to determine whether to output the data point for debugging or not
			if pred_argument != None:
				if ((index_actual != index_pred) or type (pred_argument [0]) == type (list ())) and argument == "process":
					output = True
		# invoking post processing functions
		new_arg_dict = arg_dict
		if output:
			print (str (title ["predicted_events"] [0] [0]))
			print (str (title ["events"] [0] [0]))
		new_arg_dict = fixArg2 (token_list, new_arg_dict, verbs)
		# Add the corrected new_arg_dict to the new_json_list variable
		new_json = dict ()
		new_json ["doc_key"] = title ["doc_key"]
		new_json ["dataset"] = title ["dataset"]
		new_json ["sentences"] = title ["sentences"]
		# For the actual an updated version of the annotations is being used to be consistent with changes in annotation strategy for post-process evaluation
		for updated_annotation_json in updated_annotation_json_list:
			if updated_annotation_json ["doc_key"] == title ["doc_key"]:
				new_json ["events"] = updated_annotation_json ["events"]
		# Post processed predictions
		post_processed_preds = [[[]]]
		for label in new_arg_dict:
			print (label)
			if label in argument_scores:
				print (argument_scores [label])
			elif label in new_arg_dict:
				argument_scores [label] = ("18.5001", "1.0")
			print (new_arg_dict [label])
			if label == "trigger":
				post_processed_preds [0] [0].append ([int (new_arg_dict [label]), label, float (argument_scores [label] [0]), float (argument_scores [label] [1])])
			else:
				post_processed_preds [0] [0].append ([int (new_arg_dict [label] [0]), int (new_arg_dict [label] [1]), label, float (argument_scores [label] [0]), float (argument_scores [label] [1])])
		new_json ["predicted_events"] = post_processed_preds
		new_json_list.append (new_json)
		# output for debugging and testing performance
		if output:
			print (str ("PMID: " + title ["doc_key"]))
			temp = ""
			for i in range (0, len (title ["sentences"] [0])):
				temp += title ["sentences"] [0] [i]
				temp += " "
			print (str ("Title: " + temp))
			# Print out argument 2
			temp = ""
			if "process" in new_arg_dict:
				if type (new_arg_dict ["process"] [0]) == type (list ()):
					for item in new_arg_dict ["process"]:
						for i in range (int (item [0]), int (item [1]) + 1):
							temp += title ["sentences"] [0] [i]
							temp += " "
						print (str ("process predicted: " + temp))
						temp = ""
				else:
					for i in range (int (new_arg_dict ["process"] [0]), int (new_arg_dict ["process"] [1]) + 1):
						temp += title ["sentences"] [0] [i]
						temp += " "
					print (str ("process predicted: " + temp))
				temp = ""
			if "process" in act_arg_dict:
				for i in range (int (act_arg_dict ["process"] [0]), int (act_arg_dict ["process"] [1]) + 1):
					temp += title ["sentences"] [0] [i]
					temp += " "
			print (str ("process actual: " + temp))
			# Print out argument 3
			temp = ""
			if "location" in new_arg_dict:
				if type (new_arg_dict ["location"] [0]) == type (list ()):
					for item in new_arg_dict ["location"]:
						for i in range (int (item [0]), int (item [1]) + 1):
							temp += title ["sentences"] [0] [i]
							temp += " "
						print (str ("location predicted: " + temp))
						temp = ""
				else:
					for i in range (int (new_arg_dict ["location"] [0]), int (new_arg_dict ["location"] [1]) + 1):
						temp += title ["sentences"] [0] [i]
						temp += " "
					print (str ("location predicted: " + temp))
			temp = ""
			if "location" in act_arg_dict:
				#print (str (act_arg_dict ["location"]))
				for i in range (int (act_arg_dict ["location"] [0]), int (act_arg_dict ["location"] [1]) + 1):
					temp += title ["sentences"] [0] [i]
					temp += " "
			print (str ("location actual: " + temp))
			print ("\n")
		elif "process" in arg_dict:
			if (arg_dict ["process"] != new_arg_dict ["process"]):
				print (str ("PMID: " + title ["doc_key"]))
				temp = ""
				for i in range (0, len (title ["sentences"] [0])):
					temp += title ["sentences"] [0] [i]
					temp += " "
				print (str ("Title: " + temp))
				# Print out argument 2
				temp = ""
				if "process" in new_arg_dict:
					for i in range (int (new_arg_dict ["process"] [0]), int (new_arg_dict ["process"] [1]) + 1):
						temp += title ["sentences"] [0] [i]
						temp += " "
				print (str ("process predicted: " + temp))
				temp = ""
				if "process" in act_arg_dict:
					for i in range (int (act_arg_dict ["process"] [0]), int (act_arg_dict ["process"] [1]) + 1):
						temp += title ["sentences"] [0] [i]
						temp += " "
				print (str ("process actual: " + temp))
				# Print out argument 3
				temp = ""
				if "location" in new_arg_dict:
					#print (str (new_arg_dict ["location"]))
					for i in range (int (new_arg_dict ["location"] [0]), int (new_arg_dict ["location"] [1]) + 1):
						temp += title ["sentences"] [0] [i]
						temp += " "
				print (str ("location predicted: " + temp))
				temp = ""
				if "location" in act_arg_dict:
					#print (str (act_arg_dict ["location"]))
					for i in range (int (act_arg_dict ["location"] [0]), int (act_arg_dict ["location"] [1]) + 1):
						temp += title ["sentences"] [0] [i]
						temp += " "
				print (str ("location actual: " + temp))
				print ("\n")
# Produce output as a single post-processed predictions json file
file_name = "C:\\users\\David\\Projects\\Title-Based-Molecular-Regulation-Event-Extraction\\data\\no_arg4\\5-fold_predictions\\PostProcessedPredictions.jsonl"
output = list ()
for item in new_json_list:
	output.append (str (json.dumps (item) + "\n"))
with open (file_name, 'w') as writing:
	writing.writelines (output)
print ("DONE!!!")