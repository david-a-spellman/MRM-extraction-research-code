import json

def produce_k_fold_metrics (k, directory, file_list):
	# The dictionary that will hold the metrics averaged across all folds at the end of the function, will be written to the directory at the end
	final_json = dict ()
	for file in file_list:
		file_name = file
		# read each file to accumulate the metrics averaged across all k folds
		temp_json = dict ()
		with open (file_name, 'r') as reading:
			temp_json = json.load (reading)
		for key in temp_json:
			key_fragment_list = key.split ("_")
			new_key = key_fragment_list [0]
			new_key += "_averaged"
			for j in range (1, len (key_fragment_list)):
				new_key += "_"
				new_key += key_fragment_list [j]
			if not new_key in final_json:
				final_json [new_key] = 0
			final_json [new_key] += temp_json [key]
	# Now average each accumulated metric by the number of folds
	for key in final_json:
		final_json [key] = (final_json [key] / k)
	print (str (final_json))
	file_name = str (directory + "metrics_" + str (k) + "-fold_all_models.json")
	with open (file_name, 'w') as writing:
		json.dump (final_json, writing)
	print (str ("done producing averaged metrics file for all " + str (k) + " folds."))
	print (str ("The output file is called: " + file_name))

# testing with 3-fold
#k = 3
#path = "C:\\data\\evaluations\\"
#produce_k_fold_metrics (k, path)