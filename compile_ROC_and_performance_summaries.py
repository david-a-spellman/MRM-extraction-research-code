from ProduceROCInputs import *
import json
import os
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

# Creating output files for summaries and ROC/AUC input data
"""
path = ""
f3_list = list ()
for i in range (1, 4):
	f3_list.append (str (path + "results_test_3-fold_CV_I" + str (i) + ".jsonl"))
"""
bert_model = "1"
path = str ("C:\\data\\ComparisonWithoutCL_" + bert_model + "\\5-fold_predictions\\")
f5_list = list ()
for i in range (1, 6):
	f5_list.append (str (path + "fold_" + str (i) + "_predictions.jsonl"))
# Make corrections to duplicated arguments in predictions, so that only the best predictions is used
f5_list = cleanUpPredictions (f5_list)

"""
path = "C:\\data\\10-fold_predictions\\"
f10_list = list ()
for i in range (1, 11):
	f10_list.append (str (path + "fold_" + str (i) + "_predictions.jsonl"))
"""

#f3_dir = "C:\\data\\3-fold_performance_summary\\"
f5_dir = str ("C:\\data\\ComparisonWithoutCL_" + bert_model + "\\5-fold_performance_summary\\")
#f10_dir = "C:\\data\\10-fold_performance_summary\\"

#cv3_list = create_ROC_AUC_input_lists (f3_list, f3_dir)
cv5_list = create_ROC_AUC_input_lists (f5_list, f5_dir)
#cv10_list = create_ROC_AUC_input_lists (f10_list, f10_dir)

# Variables for containing the plotting data for ROC
#data_3f_roc = dict ()
data_5f_roc = dict ()
#data_10f_roc = dict ()

# Now for producing the ROC curves
# keys for each dictionary
keys = ["trigger", "argument1", "argument2", "argument3", "argument5"]

# ROC/AUC for 3 fold CV
"""
auc_3f_cv = dict ()
auc_3f_cv_averaged = dict ()
for key in keys:
	data_3f_roc [key] = list ()
	auc_3f_cv [key] = list ()
	auc_3f_cv_averaged [key] = -1
	for file_name in cv3_list:
		if key in file_name:
			roc_auc_input = list ()
			with open (file_name, 'r') as reading:
				roc_auc_input = json.load (reading)
			y_true = list ()
			y_pred = list ()
			for item in roc_auc_input:
				y_true.append (item [0])
				y_pred.append (item [1])
			print (str (str (y_pred) + "\n\n\n\n\n"))
			print (str (str (y_true) + "\n\n\n\n\n"))
			auc_3f_cv [key].append (roc_auc_score (y_true, y_pred))
			y_true = np.array (y_true)
			y_pred = np.array (y_pred)
			print (str (str (type (y_pred)) + "\n\n\n\n\n"))
			print (str (str (type (y_true)) + "\n\n\n\n\n"))
			data_3f_roc [key].append (roc_curve (y_true, y_pred, drop_intermediate = False))
			data_3f_roc [key].append ((y_true, y_pred))
	total = 0
	for auc in auc_3f_cv [key]:
		total += auc
	averaged_auc = (total / len (auc_3f_cv [key]))
	auc_3f_cv_averaged [key] = averaged_auc
total = 0
for key in auc_3f_cv_averaged:
	total += auc_3f_cv_averaged [key]
auc_3f_cv_averaged ["averaged_across_all"] = (total / len (auc_3f_cv_averaged))
print (str (auc_3f_cv_averaged))
"""

# ROC/AUC for 5 fold CV
auc_5f_cv = dict ()
auc_5f_cv_averaged = dict ()
for key in keys:
	data_5f_roc [key] = list ()
	auc_5f_cv [key] = list ()
	auc_5f_cv_averaged [key] = -1
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
			print (str (y_pred))
			if not '0' in y_true:
				y_true [-1] = 0
			auc_5f_cv [key].append (roc_auc_score (y_true, y_pred))
			#data_5f_roc [key].append (roc_curve (np.array (y_true), np.array (y_pred), drop_intermediate = False))
			data_5f_roc [key].append ((y_true, y_pred))
	total = 0
	for auc in auc_5f_cv [key]:
		total += auc
	averaged_auc = (total / len (auc_5f_cv [key]))
	auc_5f_cv_averaged [key] = averaged_auc
total = 0
for key in auc_5f_cv_averaged:
	total += auc_5f_cv_averaged [key]
auc_5f_cv_averaged ["averaged_across_all"] = (total / len (auc_5f_cv_averaged))
print (str (auc_5f_cv_averaged))

# ROC/AUC for 10 fold CV
"""
auc_10f_cv = dict ()
auc_10f_cv_averaged = dict ()
for key in keys:
	data_10f_roc [key] = list ()
	auc_10f_cv [key] = list ()
	auc_10f_cv_averaged [key] = -1
	for file_name in cv10_list:
		if key in file_name:
			roc_auc_input = list ()
			with open (file_name, 'r') as reading:
				roc_auc_input = json.load (reading)
			y_true = list ()
			y_pred = list ()
			for item in roc_auc_input:
				y_true.append (item [0])
				y_pred.append (item [1])
			# For now just skip folds where all predictions are perfect because in the case where all actual are 1's sklearn will barf
			zero = 0
			if not zero in y_true:
				#print (len (y_true))
				#print (len (y_pred))
				#print (str (y_true))
				#print (str (y_pred))
#				temp = y_pred
#				y_pred = list ()
#				for value in temp:
#					y_pred.append (value - 0.01)
				continue
			else:
				print (str (y_pred))
				auc_10f_cv [key].append (roc_auc_score (y_true, y_pred))
				data_10f_roc [key].append (roc_curve (np.array (y_true), np.array (y_pred), drop_intermediate = False))
				data_10f_roc [key].append ((y_true, y_pred))
	total = 0
	for auc in auc_10f_cv [key]:
		total += auc
	averaged_auc = (total / len (auc_10f_cv [key]))
	auc_10f_cv_averaged [key] = averaged_auc
total = 0
for key in auc_10f_cv_averaged:
	total += auc_10f_cv_averaged [key]
auc_10f_cv_averaged ["averaged_across_all"] = (total / len (auc_10f_cv_averaged))
print (str (auc_10f_cv_averaged))
"""

# Make complete ROC AUC summary
path = "C:\\data\\ComparisonWithoutCL_1\\CK_experimental_summary\\"
if not os.path.isdir (path):
		os.mkdir (path)
file_name = str (path + "AUC_report_baseline_with_no_CL_" + bert_model + ".txt")
output = list ()
# 3 fold output
"""
output_string = "AUC for 3 fold cross validation: \n"
output_string += "{\n"
for key in auc_3f_cv_averaged:
	output_string += key
	output_string += ": "
	output_string += str (auc_3f_cv_averaged [key])
	output_string += "\n"
output_string += "}\n\n"
output.append (output_string)
"""

# 5 fold output
output_string = "AUC for 5 fold cross validation: \n"
output_string += "{\n"
# 5 fold combination
auc_5f_cv_combined = dict()
for key in data_5f_roc:
	y_true = list ()
	y_pred = list ()
	for items in data_5f_roc [key]:
		for value in items [0]:
			y_true.append (int (value))
		for value in items [1]:
			y_pred.append (value)
	auc_5f_cv_combined [key] = roc_auc_score (y_true, y_pred)
for key in auc_5f_cv_combined:
	output_string += key
	output_string += ": "
	output_string += str (auc_5f_cv_combined [key])
	output_string += "\n"
output_string += "}\n\n"
output.append (output_string)

# 10 fold output
"""
output_string = "AUC for 10 fold cross validation: \n"
output_string += "{\n"
for key in auc_10f_cv_averaged:
	output_string += key
	output_string += ": "
	output_string += str (auc_10f_cv_averaged [key])
	output_string += "\n"
output_string += "}\n\n"
output.append (output_string)
"""

# writing the output out to file
with open (file_name, 'w') as writing:
	writing.writelines (output)

# Now for producing ROC curves
# combine folds to make a single roc plot per cross validation type and per trigger/argument
# Can also make ROC curves for trigger combined with all arguments
#data_3f_roc_combined = dict ()
data_5f_roc_combined = dict ()
#data_10f_roc_combined = dict ()

# 3 fold combination and plotting
"""
for key in data_3f_roc:
	y_true = list ()
	y_pred = list ()
	for items in data_3f_roc [key]:
		for value in items [0]:
			y_true.append (int (value))
		for value in items [1]:
			y_pred.append (value)
	data_3f_roc_combined [key] = (y_true, y_pred)
"""

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

# 10 fold combination and plotting
"""
for key in data_10f_roc:
	y_true = list ()
	y_pred = list ()
	for items in data_10f_roc [key]:
		for value in items [0]:
			y_true.append (int (value))
		for value in items [1]:
			y_pred.append (value)
	data_10f_roc_combined [key] = (y_true, y_pred)
"""

# 3 fold ROC output
"""
roc_3f = dict ()
for key in data_3f_roc_combined:
	y_true = np.array (data_3f_roc_combined [key] [0])
	y_pred = np.array (data_3f_roc_combined [key] [1])
	print (str (y_true))
	print ("\n\n\n\n\n")
	print (type (y_true))
	print ("\n\n\n\n\n")
	print (str (y_pred))
	print ("\n\n\n\n\n")
	print (type (y_pred))
	print ("\n\n\n\n\n")
	roc_3f [key] = roc_curve (y_true, y_pred, drop_intermediate = False)
"""

# 5 fold ROC output
roc_5f = dict ()
for key in data_5f_roc_combined:
	y_true = np.array (data_5f_roc_combined [key] [0])
	y_pred = np.array (data_5f_roc_combined [key] [1])
	roc_5f[key] = (roc_curve (y_true, y_pred))

# 10 fold ROC output
"""
roc_10f = dict ()
for key in data_10f_roc_combined:
	y_true = np.array (data_10f_roc_combined [key] [0])
	y_pred = np.array (data_10f_roc_combined [key] [1])
	roc_10f[key] = (roc_curve (y_true, y_pred))
"""

# test the roc_curve function
#roc_curve (y_true, y_pred)

# Create and save the plots for ROC
# create 3 fold ROC plots
"""
path = "C:\\data\\3-fold_ROC_plots\\"
if not os.path.isdir (path):
	os.mkdir (path)
for key in roc_3f:
	file_name = str (path + key + "_final.png")
	plt.plot (roc_3f [key] [0], roc_3f [key] [1])
	plt.title ("3 fold cross validation " + key + " ROC")
	plt.ylabel ("true positive rate (TPR)")
	plt.xlabel ("false positive rate (FPR)")
	#plt.show ()
	plt.savefig (file_name)
	plt.cla ()
"""

# create 5 fold ROC plots
path = str ("C:\\data\\ComparisonWithoutCL_" + bert_model + "\\5-fold_ROC_plots\\")
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

# create 10 fold ROC plots
"""
path = "C:\\data\\10-fold_ROC_plots\\"
if not os.path.isdir (path):
	os.mkdir (path)
for key in roc_10f:
	file_name = str (path + key + "_final.png")
	plt.plot (roc_10f [key] [0], roc_10f [key] [1])
	plt.title ("10 fold cross validation " + key + " ROC")
	plt.ylabel ("true positive rate (TPR)")
	plt.xlabel ("false positive rate (FPR)")
	#plt.show ()
	plt.savefig (file_name)
	plt.cla ()
"""

print ("DONE!!!")