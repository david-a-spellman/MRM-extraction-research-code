import json
import os

def create_prediction_lists (file_name, out_dir):
	if not os.path.isdir (out_dir):
		os.mkdir (out_dir)
	output = list ()
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
	for item in org_json_list:
		title = item ["sentences"] [0]
		out_str = ""
		out_str += str (item ["doc_key"])
		out_str += "\n"
		out_str += str (title)
		out_str += "\n"
		if len (item ["predicted_events"] [0]) > 0:
			arguments = item ["predicted_events"] [0] [0]
		else:
			arguments = list ()
		if len (arguments) > 0:
			for argument in arguments:
				if "regulation" in argument:
					out_str += "trigger: "
					token = title [int (argument [0])]
					out_str += token
					out_str += "\n"
				elif "initiator" in argument:
					out_str += "argument 1: "
					tokens = title [int (argument [0]):int (argument [1]) + 1]
					for token in tokens:
						out_str += token
						out_str += " "
					out_str += "\n"
				elif "process" in argument:
					out_str += "argument 2: "
					tokens = title [int (argument [0]):int (argument [1]) + 1]
					for token in tokens:
						out_str += token
						out_str += " "
					out_str += "\n"
				elif "location" in argument:
					out_str += "argument 3: "
					tokens = title [int (argument [0]):int (argument [1]) + 1]
					for token in tokens:
						out_str += token
						out_str += " "
					out_str += "\n"
				elif "mechanism" in argument:
					out_str += "argument 4: "
					tokens = title [int (argument [0]):int (argument [1]) + 1]
					for token in tokens:
						out_str += token
						out_str += " "
					out_str += "\n"
				elif "target" in argument:
					out_str += "argument 5: "
					tokens = title [int (argument [0]):int (argument [1]) + 1]
					for token in tokens:
						out_str += token
						out_str += " "
					out_str += "\n"
		out_str += "\n"
		output.append (out_str)
	write_compiled_result_list (output, out_dir)

def write_compiled_result_list (output_list, output_directory):
	print (len (output_list))
	file_name = str (output_directory + "prediction_summary_dataset2.txt")
	with open (file_name, 'w') as writing:
		writing.writelines (output_list)