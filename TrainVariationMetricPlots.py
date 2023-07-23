import matplotlib.pyplot as plt

pubMedData = dict ()
clinicalData = dict ()
pubMedLargeData = dict ()

#xt = [1, 5, 10, 20, 40, 70, 100]
#yt = [0.5, 0.7, 0.8, 0.9, 1.0]
x = [1, 5, 10, 20, 40, 70, 100]
keys = ["trigger", "argument1", "argument2", "argument3", "argument5"]

pubMedData ["A 1 AUC"] = list ()
pubMedData ["A 2 AUC"] = list ()
pubMedData ["A 3 AUC"] = list ()
pubMedData ["A 4 AUC"] = list ()
pubMedData ["Trigger AUC"] = list ()

pubMedData ["A 1 Precision"] = list ()
pubMedData ["A 2 Precision"] = list ()
pubMedData ["A 3 Precision"] = list ()
pubMedData ["A 4 Precision"] = list ()
pubMedData ["Trigger Precision"] = list ()

pubMedData ["A 1 Recall"] = list ()
pubMedData ["A 2 Recall"] = list ()
pubMedData ["A 3 Recall"] = list ()
pubMedData ["A 4 Recall"] = list ()
pubMedData ["Trigger Recall"] = list ()

pubMedData ["A 1 F1"] = list ()
pubMedData ["A 2 F1"] = list ()
pubMedData ["A 3 F1"] = list ()
pubMedData ["A 4 F1"] = list ()
pubMedData ["Trigger F1"] = list ()

clinicalData ["A 1 AUC"] = list ()
clinicalData ["A 2 AUC"] = list ()
clinicalData ["A 3 AUC"] = list ()
clinicalData ["A 4 AUC"] = list ()
clinicalData ["Trigger AUC"] = list ()

clinicalData ["A 1 Precision"] = list ()
clinicalData ["A 2 Precision"] = list ()
clinicalData ["A 3 Precision"] = list ()
clinicalData ["A 4 Precision"] = list ()
clinicalData ["Trigger Precision"] = list ()

clinicalData ["A 1 Recall"] = list ()
clinicalData ["A 2 Recall"] = list ()
clinicalData ["A 3 Recall"] = list ()
clinicalData ["A 4 Recall"] = list ()
clinicalData ["Trigger Recall"] = list ()

clinicalData ["A 1 F1"] = list ()
clinicalData ["A 2 F1"] = list ()
clinicalData ["A 3 F1"] = list ()
clinicalData ["A 4 F1"] = list ()
clinicalData ["Trigger F1"] = list ()

pubMedLargeData ["A 1 AUC"] = list ()
pubMedLargeData ["A 2 AUC"] = list ()
pubMedLargeData ["A 3 AUC"] = list ()
pubMedLargeData ["A 4 AUC"] = list ()
pubMedLargeData ["Trigger AUC"] = list ()

pubMedLargeData ["A 1 Precision"] = list ()
pubMedLargeData ["A 2 Precision"] = list ()
pubMedLargeData ["A 3 Precision"] = list ()
pubMedLargeData ["A 4 Precision"] = list ()
pubMedLargeData ["Trigger Precision"] = list ()

pubMedLargeData ["A 1 Recall"] = list ()
pubMedLargeData ["A 2 Recall"] = list ()
pubMedLargeData ["A 3 Recall"] = list ()
pubMedLargeData ["A 4 Recall"] = list ()
pubMedLargeData ["Trigger Recall"] = list ()

pubMedLargeData ["A 1 F1"] = list ()
pubMedLargeData ["A 2 F1"] = list ()
pubMedLargeData ["A 3 F1"] = list ()
pubMedLargeData ["A 4 F1"] = list ()
pubMedLargeData ["Trigger F1"] = list ()

auc_file = ""
metrics_file = ""
mappings = dict ()
mappings ["argument1"] = "A 1 "
mappings ["argument2"] = "A 2 "
mappings ["argument3"] = "A 3 "
mappings ["argument5"] = "A 4 "
mappings ["trigger"] = "Trigger "
metrics = ["precision", "recall", "F1"]
met_map = dict ()
met_map ["precision"] = "Precision"
met_map ["recall"] = "Recall"
met_map ["F1"] = "F1"
bert_models = ["PubMedBert", "ClinicalPubMedBert", "PubMedBertLarge"]
title_names = {"PubMedBert" : "PBB", "ClinicalPubMedBert" : "CPB", "PubMedBertLarge" : "PBL"}
data = dict ()
data ["PubMedBert"] = pubMedData
data ["ClinicalPubMedBert"] = clinicalData
data ["PubMedBertLarge"] = pubMedLargeData
train_amounts = ["2", "11", "23", "46", "92", "161", "all"]
for bert_model in bert_models:
	for train_amount in train_amounts:
		if train_amount == "all":
			auc_file = str ("C:\\data\\ComparisonWithoutCL_" + bert_model + "\\CK_experimental_summary\\AUC_report" + bert_model + ".txt")
			metrics_file = str ("C:\\data\\ComparisonWithoutCL_" + bert_model + "\\CK_experimental_summary\\metrics_report" + bert_model + ".txt")
		else:
			auc_file = str ("C:\\data\\TrainVariation_" + bert_model + "_tests\\TrainedWith_" + train_amount + "_titles_per_fold\\CK_experimental_summary\\AUC_report" + bert_model + ".txt")
			metrics_file = str ("C:\\data\\TrainVariation_" + bert_model + "_tests\\TrainedWith_" + train_amount + "_titles_per_fold\\CK_experimental_summary\\metrics_report" + bert_model + ".txt")
		# Read AUROC values for all experiments
		lines = None
		with open (auc_file, 'r') as file:
			lines = file.readlines ()
		for line in lines:
			for key in keys:
				if key in line:
					value = line.split (": ") [-1]
					data [bert_model] [str (mappings [key] + "AUC")].append (float (value))
		lines = None
		with open (metrics_file, 'r') as file:
			lines = file.readlines ()
		for line in lines:
			for key in keys:
				for metric in metrics:
					if (key in line) and (metric in line):
						value = line.split (": ") [-1]
						data [bert_model] [str (mappings [key] + met_map [metric])].append (float (value))

metrics = ["AUC", "Precision", "Recall", "F1"]
"""
new_data = dict ()
for key in data:
	new_data [key.replace ("PubMedBert", "")] = data [key]
data = new_data
new_data = dict ()
for key in data:
	if "Clinical" in key:
		new_data [key.replace ("Clinical", "C")] = data [key]
	else:
		new_data [key] = data [key]
data = new_data
new_data = dict ()
for key in data:
	if "Large" in key:
		new_data [key.replace ("Large", "L")] = data [key]
	else:
		new_data [key] = data [key]
data = new_data

z = 1
# Produce plots
i = 0
plot_pos = [1, 3, 5, 11, 13]
for bert_model in data:
	averaged = [0, 0, 0, 0, 0, 0, 0]
	for arg in data [bert_model]:
		y = data [bert_model] [arg]
		for j in range (0, len (y)):
			averaged [j] += y [j]
		i += 1
		if i == 1:
			plt.figure (z)
		plt.subplot (3, 5, plot_pos [i - 1])
		plt.xlim (10, 100)
		plt.ylim (0.5, 1.0)
		plt.plot (x, y)
		plt.title (str (bert_model + " " + arg))
		plt.xlabel ("Percent Train")
		plt.ylabel (arg.split (" ") [-1])
		if (i % 5) == 0:
			z += 1
			for j in range (0, len (averaged)):
				averaged [j] = (averaged [j] / 5)
			plt.subplot (3, 5, 15)
			plt.xlim (10, 100)
			plt.ylim (0.5, 1.0)
			plt.plot (x, averaged)
			plt.title (str (bert_model + " " + arg.split (" ") [-1] + " Avg"))
			plt.xlabel ("Percent Train")
			plt.ylabel (str ("Avg " + arg.split (" ") [-1]))
			plt.show ()
			plt.cla ()
			plt.clf ()
			i = 0
			averaged = [0, 0, 0, 0, 0, 0, 0]
"""
print ("STARTING SUMMARIZATION GRAPH CODE!!!")
# Produce summary plot
i = 0
z = 0
k = 0
largest_trends = list ()
plot_pos = [1, 3, 5, 7, 15, 17, 19, 21, 29, 31, 33, 35]
plt.figure (1)
for bert_model in data:
	averaged = [0, 0, 0, 0, 0, 0, 0]
	for arg in data [bert_model]:
		y = data [bert_model] [arg]
		largest_trends.append ((max (y) - min (y), k))
		k += 1
		for j in range (0, len (y)):
			averaged [j] += y [j]
		i += 1
		if (i % 5) == 0:
			for j in range (0, len (averaged)):
				averaged [j] = (averaged [j] / 5)
			plt.subplot (5, 7, plot_pos [z])
			plt.xlim (0, 100)
			plt.ylim (0, 1.0)
			plt.fill_between (x, y1 = averaged, y2 = [0, 0, 0, 0, 0, 0, 0], alpha = 0.6, color = "blue")
			plt.plot (x, averaged, color = "purple")
			print (bert_model)
			plt.title (str (title_names [bert_model] + " " + arg.split (" ") [-1] + " Avg"), fontsize = 9, fontweight = "bold")
			plt.xlabel ("Percent Train", fontsize = 6)
			plt.ylabel (str ("Avg " + arg.split (" ") [-1]), fontsize = 6)
			z += 1
			i = 0
			averaged = [0, 0, 0, 0, 0, 0, 0]
plt.show ()
plt.cla ()
plt.clf ()
# Sort most significant trends and take top 6
print ("Getting most significant trends!!!")
best_trends = list ()
for i in range (0, len (largest_trends)):
	for j in range (0, len (largest_trends) - i - 1):
		t1 = largest_trends [j]
		t2 = largest_trends [j + 1]
		if t2 [0] > t1 [0]:
			largest_trends [j] = t2
			largest_trends [j + 1] = t1
for i in range (0, 6):
	best_trends.append (largest_trends [i] [-1])
largest_trends = best_trends
# Produce most significant trend plot
print ("Producing summary with most significant trends!!!")
i = 0
z = 0
plot_pos = [1, 3, 5, 11, 13, 15]
plt.figure (2)
for bert_model in data:
	for arg in data [bert_model]:
		y = data [bert_model] [arg]
		if i in largest_trends:
			plt.subplot (3, 5, plot_pos [z])
			plt.xlim (0, 100)
			plt.ylim (0, 1.0)
			plt.fill_between (x, y1 = y, y2 = [0, 0, 0, 0, 0, 0, 0], alpha = 0.6, color = "blue")
			plt.plot (x, y, color = "purple")
			plt.title (str (title_names [bert_model]  + " " + arg), fontsize = 9, fontweight = "bold")
			plt.xlabel ("Percent Train", fontsize = 6)
			plt.ylabel (arg.split (" ") [-1], fontsize = 6)
			z += 1
		i += 1
plt.show ()
plt.cla ()
plt.clf ()
print ("DONE!!!")