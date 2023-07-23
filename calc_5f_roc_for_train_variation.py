from PredictionWiseProduceROCInputs import *
import json
import os
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

# Creating output files for summaries and ROC/AUC input data

experiment_set = "TrainVariation_"
bert_model = "PubMedBert"
train_count = "11"
path = str ("C:\\data\\" + experiment_set + bert_model + "_tests\\TrainedWith_" + train_count + "_titles_per_fold\\5-fold_predictions\\")
f5_list = list ()
for i in range (1, 6):
	f5_list.append (str (path + "fold_" + str (i) + "_predictions.jsonl"))
# Make corrections to duplicated arguments in predictions, so that only the best predictions is used
f5_list = cleanUpPredictions (f5_list)

f5_dir = str ("C:\\data\\" + experiment_set + bert_model + "_tests\\TrainedWith_" + train_count + "_titles_per_fold\\5-fold_performance_summary\\")

cv5_list = create_ROC_AUC_input_lists (f5_list, f5_dir)
cv5_fn_list = createRecall_input_lists (f5_list, f5_dir)

# Variables for containing the plotting data for ROC
data_5f_roc = dict ()

# Now for producing the ROC curves
# keys for each dictionary
keys = ["trigger", "argument1", "argument2", "argument3", "argument5"]



# ROC/AUC for 5 fold CV
auc_5f_cv = dict ()
fn_5f_cv = dict ()
metrics_5f_cv = dict ()
for key in keys:
	data_5f_roc [key] = list ()
	auc_5f_cv [key] = list ()
	fn_5f_cv [key] = list ()
	for file_name in cv5_list:
		if key in file_name:
			roc_auc_input = list ()
			with open (file_name, 'r') as reading:
				roc_auc_input = json.load (reading)
			y_true = list ()
			y_pred = list ()
			for item in roc_auc_input:
				y_true.append (item [0])
				y_pred.append (item [1])
			data_5f_roc [key].append ((y_true, y_pred))
	for file_name in cv5_fn_list:
		if key in file_name:
			recall_input = list ()
			with open (file_name, 'r') as reading:
				recall_input = json.load (reading)
			for val in recall_input:
				fn_5f_cv [key].append (val)



# Make complete ROC AUC summary
path = "C:\\data\\" + experiment_set + bert_model + "_tests\\TrainedWith_" + train_count + "_titles_per_fold\\CK_experimental_summary\\"
if not os.path.isdir (path):
		os.mkdir (path)
file_name = str (path + "AUC_report" + bert_model + ".txt")
output = list ()


# 5 fold output
output_string = "AUC for 5 fold cross validation: \n"
output_string += "{\n"
# 5 fold combination
auc_5f_cv_combined = dict()
for key in data_5f_roc:
	y_true = list ()
	y_pred = list ()
	for items in data_5f_roc [key]:
		#print (items [0])
		#print (items [1])
		#print (len (items [0]))
		#print (len (items [1]))
		for value in items [0]:
			y_true.append (int (value))
		for value in items [1]:
			y_pred.append (float (value))
	print(key)
	print("Number of predictions: " + str(len(y_true)))
	print("Number of predictions: " + str(len(y_pred)))
	if not 1 in y_true:
		auc_5f_cv_combined [key] = 0
	elif not 0 in y_true:
		auc_5f_cv_combined [key] = 1
	else:
		auc_5f_cv_combined [key] = roc_auc_score (y_true, y_pred)
	print("Combined AUC: " + str(auc_5f_cv_combined [key]))
for key in auc_5f_cv_combined:
	output_string += key
	output_string += ": "
	output_string += str (auc_5f_cv_combined [key])
	output_string += "\n"
output_string += "}\n\n"
output.append (output_string)


# writing the output out to file
with open (file_name, 'w') as writing:
	writing.writelines (output)

# Make complete precision, recall, and F1 summary
file_name = str (path + "metrics_report" + bert_model + ".txt")
output = list ()
precisions = dict ()
recalls = dict ()
f1s = dict ()

# 5 fold output
output_string = "precision for 5 fold cross validation: \n"
output_string += "{\n"
# 5 fold combination
auc_5f_cv_combined = dict()
for key in data_5f_roc:
	tp = list ()
	for items in data_5f_roc [key]:
		for value in items [0]:
			tp.append (value)
	fn = fn_5f_cv [key]
	print(key)
	print("Number of predictions: " + str(len(tp)))
	print("Number of labels: " + str(len(fn)))
	#print (tp)
	#print (fn)
	if len (tp) == 0:
		precisions [key] = 0
	else:
		precisions [key] = calculatePrecision (tp)
	recalls [key] = calculateRecall (fn, tp)
	if (recalls [key] > 0) and (precisions [key] > 0):
		f1s [key] = calculateF1 (precisions [key], recalls [key])
	else:
		f1s [key] = 0
	print("Combined F1: " + str(f1s [key]))
for key in precisions:
	output_string += "\""
	output_string += key
	output_string += " precision\""
	output_string += ": "
	output_string += str (precisions [key])
	output_string += "\n"
output_string += "}\n\n"
output_string += "recall for 5 fold cross validation: \n"
output_string += "{\n"
for key in recalls:
	output_string += "\""
	output_string += key
	output_string += " recall\""
	output_string += ": "
	output_string += str (recalls [key])
	output_string += "\n"
output_string += "}\n\n"
output_string += "F1 for 5 fold cross validation: \n"
output_string += "{\n"
for key in f1s:
	output_string += "\""
	output_string += key
	output_string += " F1\""
	output_string += ": "
	output_string += str (f1s [key])
	output_string += "\n"
output_string += "}\n\n"
output.append (output_string)


# writing the output out to file
with open (file_name, 'w') as writing:
	writing.writelines (output)

# Now for producing ROC curves
# combine folds to make a single roc plot per cross validation type and per trigger/argument
# Can also make ROC curves for trigger combined with all arguments
data_5f_roc_combined = dict ()


# 5 fold combination and plotting
for key in data_5f_roc:
	y_true = list ()
	y_pred = list ()
	for items in data_5f_roc [key]:
		for value in items [0]:
			y_true.append (int (value))
		for value in items [1]:
			y_pred.append (value)
	data_5f_roc_combined [key] = (y_true, y_pred)


# 5 fold ROC output
roc_5f = dict ()
for key in data_5f_roc_combined:
	y_true = np.array (data_5f_roc_combined [key] [0])
	y_pred = np.array (data_5f_roc_combined [key] [1])
	if ('1' in y_true) and ('0' in y_true):
		roc_5f[key] = (roc_curve (y_true, y_pred))


# Create and save the plots for ROC
# create 5 fold ROC plots
path = str ("C:\\data\\" + experiment_set + bert_model + "_tests\\TrainedWith_" + train_count + "_titles_per_fold\\5-fold_ROC_plots\\")
if not os.path.isdir (path):
	os.mkdir (path)
for key in roc_5f:
	file_name = str (path + key + ".png")
	plt.plot (roc_5f [key] [0], roc_5f [key] [1])
	plt.title ("5 fold cross validation " + key + " ROC")
	plt.ylabel ("true positive rate (TPR)")
	plt.xlabel ("false positive rate (FPR)")
	#plt.show ()
	plt.savefig (file_name)
	plt.cla ()

print ("DONE!!!")