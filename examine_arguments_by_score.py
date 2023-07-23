# script to produce sorted csv files for each argument with the rows sorted by the prediction score output by the model
import json
from collections import OrderedDict
from ProduceROCInputs import inverse_logit
arguments = ["initiator", "process", "location", "target"]
csv_strings = dict ()
csv_strings ["trigger"] = list ()
for argument in arguments:
	csv_strings [argument] = list ()
file_list = ["C:\\data\\no_arg4\\5-fold_predictions\\fold_1_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_2_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_3_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_4_predictions.jsonl", "C:\\data\\no_arg4\\5-fold_predictions\\fold_5_predictions.jsonl"]
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
		point_string = ""
		if len (title ["predicted_events"] [0]) > 0:
			pred_trigger = title ["predicted_events"] [0] [0] [0]
		else:
			continue
		point_string += str (inverse_logit (float (pred_trigger [2])))
		actual_trigger = title ["events"] [0] [0] [0]
		index_pred = pred_trigger [0]
		index_actual = actual_trigger [0]
		point_string += ","
		if index_pred != "":
			point_string += title ["sentences"] [0] [int (index_pred)]
		point_string += ","
		point_string += title ["sentences"] [0] [int (index_actual)]
		point_string += ","
		point_string += str (title ["doc_key"])
		point_string += ","
		for token in title ["sentences"] [0]:
			if token == ",":
				continue
			elif token == ".":
				point_string += token
			else:
				point_string += token
				point_string += ' '
		point_string += ",\n"
		if (index_actual != index_pred):
			csv_strings ["trigger"].append (point_string)
		for argument in arguments:
			pred_arguments = title ["predicted_events"] [0] [0]
			pred_argument = None
			for i in range (1, len (pred_arguments)):
				if argument in pred_arguments [i]:
					pred_argument = pred_arguments [i]
			actual_arguments = title ["events"] [0] [0]
			actual_argument = None
			for i in range (1, len (actual_arguments)):
				if argument in actual_arguments [i]:
					actual_argument = actual_arguments [i]
			point_string = ""
			if pred_argument != None:
				point_string += str (inverse_logit (float (pred_argument [3])))
				index_pred = (pred_argument [0], pred_argument [1])
				point_string += ","
				for token in title ["sentences"] [0] [int (index_pred [0]):int (index_pred [1]) + 1]:
					if token == ",":
						continue
					elif token == ".":
						point_string += token
					else:
						point_string += token
						point_string += ' '
				point_string += ","
				if actual_argument != None:
					index_actual = (actual_argument [0], actual_argument [1])
					for token in title ["sentences"] [0] [int (index_actual [0]):int (index_actual [1]) + 1]:
						if token == ",":
							continue
						elif token == ".":
							point_string += token
						else:
							point_string += token
							point_string += ' '
				point_string += ","
				point_string += str (title ["doc_key"])
				point_string += ","
				for token in title ["sentences"] [0]:
					if token == ",":
						continue
					elif token == ".":
						point_string += token
					else:
						point_string += token
						point_string += ' '
				point_string += ",\n"
				if (index_actual != index_pred):
					csv_strings [argument].append (point_string)
# Sort and write to file
for key in csv_strings:
	sorted_dict = dict ()
	for string in csv_strings [key]:
		sorted_dict [float (string.split (",") [0])] = string
	sorted_points = OrderedDict (sorted (sorted_dict.items ()))
	output = list ()
	output.append ("score,predicted,actual,PMID,title,\n")
	for item in sorted_points:
		output.append (sorted_points [item])
	file_name = str ("C:\\data\\no_arg4\\5-fold_predictions\\" + key + ".csv")
	with open (file_name, 'w') as writing:
		writing.writelines (output)
print ("DONE!!!")