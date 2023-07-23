from PredictionWiseProduceROCInputs import *
import json
import os
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

# Creating output files for summaries and ROC/AUC input data


experiment = "gpt3.5_incontext learning"
path = str (".\\" + experiment + "\\")
if not os.path.isdir (path):
		os.mkdir (path)
pred_list = list ()
pred_list.append (str (".\\" + experiment + ".jsonl"))
# Make corrections to duplicated arguments in predictions, so that only the best predictions is used
pred_list = cleanUpPredictions (pred_list)

pred_dir = str (".\\" + experiment + "\\Chat_GPT_performance_summary\\")
if not os.path.isdir (pred_dir):
		os.mkdir (pred_dir)

eval_list = create_ROC_AUC_input_lists (pred_list, pred_dir)
eval_fn_list = createRecall_input_lists (pred_list, pred_dir)

# Variables for containing the plotting data for ROC
data_roc = dict ()

# Now for producing the ROC curves
# keys for each dictionary
keys = ["trigger", "argument1", "argument2", "argument3", "argument5"]



# ROC/AUC 
auc_pred = dict ()
fn_pred = dict ()
metrics_pred = dict ()
for key in keys:
	data_roc [key] = list ()
	auc_pred [key] = list ()
	fn_pred [key] = list ()
	for file_name in eval_list:
		if key in file_name:
			roc_auc_input = list ()
			with open (file_name, 'r') as reading:
				roc_auc_input = json.load (reading)
			y_true = list ()
			y_pred = list ()
			for item in roc_auc_input:
				y_true.append (item [0])
				y_pred.append (item [1])
			data_roc [key].append ((y_true, y_pred))
	for file_name in eval_fn_list:
		if key in file_name:
			recall_input = list ()
			with open (file_name, 'r') as reading:
				recall_input = json.load (reading)
			for val in recall_input:
				fn_pred [key].append (val)



# Make complete ROC AUC summary
path = ".\\" + experiment + "\\Chat_GPT_experiment_summary\\"
if not os.path.isdir (path):
		os.mkdir (path)
file_name = str (path + "evaluation_" + experiment + ".txt")
output = list ()


# output
output_string = "AUROC: \n"
output_string += "{\n"
# combination
auc_pred_combined = dict()
for key in data_roc:
	y_true = list ()
	y_pred = list ()
	for items in data_roc [key]:
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
		auc_pred_combined [key] = 0
	elif not 0 in y_true:
		auc_pred_combined [key] = 1
	else:
		auc_pred_combined [key] = roc_auc_score (y_true, y_pred)
	print("Combined AUC: " + str(auc_pred_combined [key]))
for key in auc_pred_combined:
	output_string += key
	output_string += ": "
	output_string += str (auc_pred_combined [key])
	output_string += "\n"
output_string += "}\n\n"
output.append (output_string)


# writing the output out to file
with open (file_name, 'w') as writing:
	writing.writelines (output)

# Make complete precision, recall, and F1 summary
file_name = str (path + "evaluation_" + experiment + ".txt")
output = list ()
precisions = dict ()
recalls = dict ()
f1s = dict ()

# output
output_string = "precision: \n"
output_string += "{\n"
# combination
auc_pred_combined = dict()
for key in data_roc:
	tp = list ()
	for items in data_roc [key]:
		for value in items [0]:
			tp.append (value)
	fn = fn_pred [key]
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
output_string += "recall: \n"
output_string += "{\n"
for key in recalls:
	output_string += "\""
	output_string += key
	output_string += " recall\""
	output_string += ": "
	output_string += str (recalls [key])
	output_string += "\n"
output_string += "}\n\n"
output_string += "F1: \n"
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
# make a roc plot per trigger/argument
# Can also make ROC curves for trigger combined with all arguments
data_roc_combined = dict ()


# plotting
for key in data_roc:
	y_true = list ()
	y_pred = list ()
	for items in data_roc [key]:
		for value in items [0]:
			y_true.append (int (value))
		for value in items [1]:
			y_pred.append (value)
	data_roc_combined [key] = (y_true, y_pred)


# ROC output
roc_pred = dict ()
for key in data_roc_combined:
	y_true = np.array (data_roc_combined [key] [0])
	y_pred = np.array (data_roc_combined [key] [1])
	if ('1' in y_true) and ('0' in y_true):
		roc_pred[key] = (roc_curve (y_true, y_pred))


# Create and save the plots for ROC
# create AUROC plots
path = str (".\\" + experiment + "\\ROC_plots\\")
if not os.path.isdir (path):
	os.mkdir (path)
for key in roc_pred:
	file_name = str (path + key + ".png")
	plt.plot (roc_pred [key] [0], roc_pred [key] [1])
	plt.title ("Chat GPT " + key + " ROC")
	plt.ylabel ("true positive rate (TPR)")
	plt.xlabel ("false positive rate (FPR)")
	#plt.show ()
	plt.savefig (file_name)
	plt.cla ()

print ("DONE!!!")