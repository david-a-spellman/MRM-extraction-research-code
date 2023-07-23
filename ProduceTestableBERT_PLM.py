import json
import random
from NestedKFCVMetrics import produce_k_fold_metrics
from NestedKFCVFileOperations import *

path = "/mnt/c/data/Baseline_models/PubMedBERT/"
file_name = str ("/mnt/c/data/" + "DIGGIE++_arg4_free_input_titles.json")

json_strings = list ()
org_json_list = list ()
with open (file_name, 'r') as reading:
	json_strings = reading.readlines ()
count = 1
for string in json_strings:
	print (str (count))
	if "\n" in string:
		#print ("contains endline character")
		new_string = string.replace ("\n", "")
		org_json_list.append (json.loads (new_string))
		count += 1
		continue
	org_json_list.append (json.loads (string))
	count += 1
#print (str (org_json_list))
k = 1
"""
while k == -1:
	string_k = input ("Please enter a number of folds between 3 and " + str (len (org_json_list)) + ": ")
	if str.isnumeric (string_k):
		k = int (string_k)
	if k < 3 or k >= len (org_json_list):
		k = -1
"""
random.shuffle (org_json_list)
random.shuffle (org_json_list)
random.shuffle (org_json_list)
folds = list ()
for x in range (0, 3):
	folds.append (list ())
i = 0
for item in org_json_list:
	index = i
	if index > 1:
		index = 2
	folds [index].append (item)
	i += 1

# Print the lengths of each dataset
for i in range (0, len (folds)):
	print (str (len (folds [i])))

file_list = make_fold_files (folds, str (path + str (k) + "-fold_data/"))
metric_files = list ()
for i in range (0, k):
	test = file_list [-1]
	if (i + 1) == k:
		dev = file_list [0]
	else:
		dev = file_list [i + 1]
	train_list = list (set (file_list) - set ([test, dev]))
	train = make_temp_train_file (train_list, str (path + str (k) + "-fold_data/"))
	print ("fold " + str (i))
	print ("test file: " + test)
	print ("validation file: " + dev)
	print ("Rest of splits went into the temp training file: " + train)
	print ("configuring and launching training on fold " + str (i))

	# Modifying k-fold reusable jsonnet file for configuring training of each fold
	jsonnet_file = "/mnt/c/Users/David/Projects/dygiepp/training_config/k-fold_CV.jsonnet"
	modify_jsonnet_file (jsonnet_file, train, dev, test)
	# Now launch the bash scripts with python
	jsonnet_name = jsonnet_file.split ("/") [-1].split (".") [0]
	command = str ("bash scripts/train.sh " + jsonnet_name)
	print ("Running command: " + command)
	os.system (command)
	# now copying files and clearing out old directory from training
#	# command to copy model files to models_saved
#	command = str ("cp -r models/" + jsonnet_name + " models_saved")
#	print ("Running command: " + command)
#	os.system (command)
	# command to rename model files
#	pretrained_model_dir = str (str ("models_saved/" + str (k) + "-f_cv") + "fold_" + str (i + 1))
#	command = str ("mv " + str ("models_saved/" + "k-f_CV") + " " + pretrained_model_dir)
#	print ("Running command: " + command)
#	os.system (command)
	# command to coppy pretrained model to a pretrained directory
	if not os.path.isdir (str ("pretrained/" + str (k) + "-f_cv")):
		os.mkdir (str ("pretrained/" + str (k) + "-f_cv"))
	command = str ("cp models/" + jsonnet_name + "/model.tar.gz pretrained/" + str (k) + "-f_cv")
	print ("Running command: " + command)
	os.system (command)
	# command to rename model file
	pretrained_model = str (str ("pretrained/" + str (k) + "-f_cv/") + "fold_" + str (i + 1) + ".tar.gz")
	command = str ("mv " + str ("pretrained/" + str (k) + "-f_cv/") + "model.tar.gz " + pretrained_model)
	print ("Running command: " + command)
	os.system (command)
	# remove the models directory
	command = str ("rm -r models")
	print ("Running command: " + command)
	os.system (command)
	# Now use AllenNLP to run evaluation and prediction
	metrics_directory = str (path + str (k) + "-fold_metrics/")
	if not os.path.isdir (metrics_directory):
		os.mkdir (metrics_directory)
	metrics_file = str (metrics_directory + "fold_" + str (i + 1) + "_metrics.json")
	command = str ("allennlp evaluate \\\n  " + pretrained_model + " \\\n  " + test + " \\\n  --cuda-device 0  \\\n  --include-package dygie \\\n  --output-file " + metrics_file)
	print ("Running command: " + command)
	os.system (command)
	predictions_directory = str (path + str (k) + "-fold_predictions/")
	if not os.path.isdir (predictions_directory):
		os.mkdir (predictions_directory)
	predictions_file = str (predictions_directory + "fold_" + str (i + 1) + "_predictions.jsonl")
	command = str ("allennlp predict \\\n  " + pretrained_model + " \\\n  " + test + " \\\n  --predictor dygie \\\n  --include-package dygie \\\n  --use-dataset-reader \\\n  --output-file " + predictions_file + " \\\n  --cuda-device 0 \\\n  --silent")
	print ("Running command: " + command)
	os.system (command)
	metric_files.append (metrics_file)

# Now produce final average metrics file for the k folds

#k = 5
#metric_files = ["/mnt/c/data/ComparisonWithoutCL_1/5-fold_metrics/fold_1_metrics.json", "/mnt/c/data/ComparisonWithoutCL_1/5-fold_metrics/fold_2_metrics.json", "/mnt/c/data/ComparisonWithoutCL_1/5-fold_metrics/fold_3_metrics.json", "/mnt/c/data/ComparisonWithoutCL_1/5-fold_metrics/fold_4_metrics.json", "/mnt/c/data/ComparisonWithoutCL_1/5-fold_metrics/fold_5_metrics.json"]
print ("Done with all folds!!! Now producing average metrics file!!!")
if not os.path.isdir (str (path + "evaluations/")):
	os.mkdir (str (path + "evaluations/"))
produce_k_fold_metrics (k, str (path + "evaluations/"), metric_files)
print ("DONE!!!")