import json

org_json = dict ()
file_name = "C:\\data\\Arg4FreeNewTriggerPunctuated.json"
with open (file_name, 'r') as reading:
	org_json = json.load (reading)
new_json = org_json
file_name = "C:\\data\\CleanedLabelingOfPMTitles.csv"
lines = list ()
with open (file_name, 'r') as reading:
	lines = reading.readlines ()

for id in org_json:
	for line in lines:
		if id in line:
			new_json [id] ["trigger"] = line.split (",") [7]
			labels = org_json [id] ["annotation"] [0]
			title = org_json [id] ["document"]
			for arg in labels:
				if type (labels [arg]) != type (str ()):
					#print (str (labels [arg]))
					new_arg = labels [arg] [0]
					if len (new_arg.split (" ")) <= 1:
						continue
					first_word = new_arg.split (" ") [0]
					last_word = new_arg.split (" ") [-1]
				elif len (labels [arg].split (" ")) <= 1:
					continue
				else:
					first_word = labels [arg].split (" ") [0]
					last_word = labels [arg].split (" ") [-1]
				if not first_word in title:
					new_char = first_word [:1].upper ()
					first_word = str (new_char + first_word [1:])
				if not last_word in title:
					new_char = last_word [:1].upper ()
					last_word = str (new_char + last_word [1:])
				if len (last_word) <= 1 or len (first_word) <= 1:
					last_word = str (" " + last_word)
				#print ("first word: " + first_word)
				#print ("last word: " + last_word)
				#print (title)
				start = title.index (first_word)
				if not last_word in title:
					print (str (title))
					print (last_word)
					last_word = input ("Give a fix to this last word of the annotated argument that does not match the title: ")
				end = title.index (last_word) + len (last_word)
				new_label = title [start:end]
				if type (new_label) == type (list ()):
					new_label = new_label [0]
				new_label = str (str (new_label))
				new_label.replace ("[", "")
				new_label.replace ("]", "")
				new_json [id] ["annotation"] [0] [arg] = new_label

file_name = "C:\\data\\Cleaned_sciERC_input_no_arg4.json"
with open (file_name, 'w') as writing:
	json.dump (new_json, writing)
print ("DONE!!!")