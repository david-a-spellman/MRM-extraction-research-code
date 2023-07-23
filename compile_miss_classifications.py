import json

file_name = "C:\\data\\cancer_knowledge_predictions\\results_test_set1.jsonl"
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
# Itterate over each title in the test set and compare event entries to event prediction entries
# If all match then output that the predictions were perfect, else output the miss predictions and what they should have been
output = list ()
for title in org_json_list:
	output.append (str ("PMID: " + title ["doc_key"] + "\n" + str (title ["sentences"]) + "\n"))
	labels = title ["events"] [0] [0]
	print (str (type (title ["predicted_events"])))
	predictions = title ["predicted_events"] [0] [0]
	label_trigger = None
	prediction_trigger = None
	label_args = list ()
	prediction_args = list ()
	for i in range (0, len (labels)):
		if i == 0:
			label_trigger = labels [i] [0]
		else:
			label_args.append (labels [i] [2])
	for i in range (0, len (predictions)):
		if i == 0:
			prediction_trigger = predictions [i] [0]
		else:
			prediction_args.append (predictions [i] [2])
	if label_trigger == prediction_trigger and label_args == prediction_args:
		perfect = True
		for i in range (0, len (label_args)):
			start_lab
			end_lab
			start_pred
			end_pred
			if start_lab != start_pred or end_lab != end_pred:
				perfect = False
		if perfect:
			output.append ("PERFECT!\n\n")
		else:
			for i in range (1, len (label_args)):
				label = ""
				prediction = ""
				for j in range (int (labels [i] [0]), int (labels [i] [1]) + 1):
					label += title ["sentences"] [0] [j]
					label += " "
				for j in range (int (predictions [i] [0]), int (predictions [i] [1]) + 1):
					prediction += title ["sentences"] [0] [j]
					prediction += " "
				if label != prediction:
					output.append (str ("predicted " + predictions [i] [2] + " is: " + predicted + "\n"))
					output.append (str ("actual " + labels [i] [2] + " is: " + label + "\n\n"))
	else:
		if label_trigger != prediction_trigger:
			output.append (str ("predicted trigger word is " + predicted_trigger))
			output.append (str ("actual trigger word is " + label_trigger))
		if prediction_args != label_args:
			for item in prediction_args:
				if not item in label_args:
					start = -1
					end = -1
					for segment in predictions:
						if item in segment:
							start = int (segment [0])
							end = int (segment [1])
					output.append (str ("there should be no " + item + " in this prediction\n" + str (title ["sentences"] [0] [start:(end + 1)]) + " is not a " + item + "\n"))
			for item in label_args:
				if not item in prediction_args:
					start = -1
					end = -1
					for segment in labels:
						if item in segment:
							start = int (segment [0])
							end = int (segment [1])
					output.append (str ("there should be a " + item + " in this prediction\nthe " + item + " should be " + str (title ["sentences"] [0] [start:(end + 1)]) + "\n"))
			same = list ()
			for item in prediction_args:
				if item in label_args:
					same.append (item)
			for item in same:
				i = -1
				for segment in labels:
					if item in segment:
						i = labels.index (segment)
				j = -1
				for segment in predictions:
					if item in segment:
						j = predictions.index (segment)
				label = ""
				prediction = ""
				for z in range (int (labels [i] [0]), int (labels [i] [1]) + 1):
					label += title ["sentences"] [0] [z]
					label += " "
				for z in range (int (predictions [j] [0]), int (predictions [j] [1]) + 1):
					prediction += title ["sentences"] [0] [z]
					prediction += " "
				if label != prediction:
					output.append (str ("predicted " + predictions [j] [2] + " is: " + prediction + "\n"))
					output.append (str ("actual " + labels [i] [2] + " is: " + label + "\n\n"))

file_name = "C:\\data\\cancer_knowledge_predictions\\summarized_results_test_set1.txt"
with open (file_name, 'w') as writing:
	writing.writelines (output)
print ("DONE!!!")