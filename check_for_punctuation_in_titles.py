import json

file_name = "C:\\data\\auto_generated_events.csv"

lines = list ()
with open (file_name, 'r') as reading:
	lines = reading.readlines ()
file_name = "C:\\data\\Cleaned_Temp_Gen_no_arg4_new_triggers.json"
org_json = dict ()
with open (file_name, 'r') as reading:
	org_json = json.load (reading)
new_json = org_json
for id in org_json:
	last_word = org_json [id] ["document"].split (" ") [-1]
	second_last_word = org_json [id] ["document"].split (" ") [-2]
	first_word = org_json [id] ["document"].split (" ") [0]
	new_line = str ()
	for line in lines:
		if (id in line):
			if last_word.isnumeric ():
				last_word = str (" " + last_word)
			if org_json [id] ["document"].count (last_word) > 1:
				last_word = str (second_last_word + " " + last_word)
			if not last_word in line:
				print (line)
				print (last_word)
			position = line.index (last_word) + len (last_word)
			if not (line [position] == "."):
				print (id)
				print (line)
				print ("first word: " + first_word)
				print ("last word: " + last_word)
				new_line = line
				new_line = str (new_line [:position] + ".")
				print ("new line: " + new_line)
				position = new_line.index (first_word)
				new_line = new_line [position:]
				new_line = new_line.replace ("\"", "")
				print (new_line)
			else:
				new_line = line
				new_line = str (new_line [:position] + ".")
				position = new_line.index (first_word)
				new_line = new_line [position:]
				new_line = new_line.replace ("\"", "")
				print (new_line)
	new_json [id] ["document"] = new_line
file_name = "C:\\data\\Arg4FreeNewTriggerPunctuated.json"
with open (file_name, 'w') as writing:
	json.dump (new_json, writing)
print ("DONE!!!")