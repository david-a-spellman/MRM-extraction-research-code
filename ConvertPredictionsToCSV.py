import json

# prescreening_predictions_on_dataset_2.jsonl

fn = "C:\\data\\prescreening_predictions_on_dataset_2.jsonl"
lines = list ()
with open (fn, 'r', encoding = "utf8") as file:
	lines = file.readlines ()
titles = list ()
for line in lines:
	titles.append (json.loads (line.replace ("\n", "")))
new_titles = list ()
for title in titles:
	if len (title ["predicted_events"] [0]) == 0:
		continue
	a1 = list ()
	a2 = list ()
	a3 = list ()
	a4 = list ()
	rv = list ()
	for pred in title ["predicted_events"] [0] [0]:
		if "initiator" in pred:
			a1.append (pred)
		elif "process" in pred:
			a2.append (pred)
		elif "location" in pred:
			a3.append (pred)
		elif "target" in pred:
			a4.append (pred)
		elif "regulation" in pred:
			rv.append (pred)
	new_preds = list ()
	index = 0
	score = 0
	for pred in a1:
		if pred [-2] > score:
			index = a1.index (pred)
			score = pred [-2]
	if len (a1) > 0:
		new_preds.append (a1 [index])
	index = 0
	score = 0
	for pred in a2:
		if pred [-2] > score:
			index = a2.index (pred)
			score = pred [-2]
	if len (a2) > 0:
		new_preds.append (a2 [index])
	index = 0
	score = 0
	for pred in a3:
		if pred [-2] > score:
			index = a3.index (pred)
			score = pred [-2]
	if len (a3) > 0:
		new_preds.append (a3 [index])
	index = 0
	score = 0
	for pred in a4:
		if pred [-2] > score:
			index = a4.index (pred)
			score = pred [-2]
	if len (a4) > 0:
		new_preds.append (a4 [index])
	index = 0
	score = 0
	for pred in rv:
		if pred [-2] > score:
			index = rv.index (pred)
			score = pred [-2]
	if len (rv) > 0:
		new_preds.append (rv [index])
	new_title = title
	new_title ["predicted_events"] [0] [0] = new_preds
	new_titles.append (new_title)
titles = new_titles

out_strs = list ()
out_strs.append ("PM_id,title,initiator (A1),process (A2),context (A3),target (A4),regulation verb (trigger),A1 logit,A2 logit,A3 logit,A4 logit,RV logit\n")
for title in titles:
	output = ""
	output += title ["doc_key"]
	output += ","
	t = title ["sentences"] [0]
	for token in t:
		if token == ",":
			continue
		if (t.index (token) == t [len (t) - 1]) and (t.index (token) == 0):
			output += token
		else:
			output += " "
			output += token
	output += ","
	if len (title ["predicted_events"] [0]) > 0:
		preds = title ["predicted_events"] [0] [0]
	else:
		preds = list ()
	if len (preds) > 5:
		print (str ("ISSUE WITH NUMBER OF PREDICTIONS FOR TITLE " + title ["doc_key"]))
		quit ()
	labels = ["initiator", "process", "location", "target"]
	for label in labels:
		for pred in preds:
			if label in pred:
				for i in range (pred [0], pred [1] + 1):
					token = t [i]
					if token == ",":
						continue
					if (t.index (token) == t [pred [1]]) and (t.index (token) == t [pred [0]]):
						output += token
					else:
						output += " "
						output += token
		output += ","
	for pred in preds:
		if ("regulation" in pred) and (t [pred [0]] != ","):
			output += t [pred [0]]
	labels.append ("regulation")
	for label in labels:
		output += ","
		for pred in preds:
			if label in pred:
				output += str (pred [-2])
	output += "\n"
	out_strs.append (output)

# "C:\\data\\dataset_2_predictions.csv"
fn = "C:\\data\\dataset_2_predictions.csv"
with open (fn, 'w', encoding = "utf8") as file:
	file.writelines (out_strs)
print ("DONE !!!")