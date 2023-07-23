import json

def csv_to_json (csv, output):
	csv_lines = list ()
	with open (csv, 'r') as csvf:
		csv_lines = csvf.readlines ()
	json_form = dict ()
	for item in csv_lines:
		items = item.split (",")
		if (items [10] == "1"):
			json_form [int (items [0])] = (items [1], items [7], (items [2], items [3], items [4], items [5], items [6]))
	with open (output, 'w') as outf:
		json.dump (json_form, outf)

csv = "C:\\data\\CleanedLabelingOfPMTitles.csv"
output = "C:\\data\\PM_title_event_labels.json"
csv_to_json (csv, output)