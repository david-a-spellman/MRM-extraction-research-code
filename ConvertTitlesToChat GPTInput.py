import json

file_name = "C:\\data\\m6A_MRM_titles_4_args_test.csv"
read_titles = "C:\\data\\Arg4FreeNewTriggerPunctuated.json"

lines = list ()
with open (file_name, 'r') as file:
	lines = file.readlines ()
titles = dict ()
with open (read_titles, 'r') as file:
	string = file.read ()
	titles = json.loads (string)
new_lines = list ()
new_lines.append (lines [0].replace (",", "\t"))
for i in range (1, len (lines)):
	line = lines [i]
	#print (line)
	if len (line) < 5:
		continue
	if line [-4] == "0":
		continue
	pmid = line [0:8]
	if not pmid in titles:
		continue
	title = titles [pmid] ["document"]
	new_line = ""
	new_line += pmid
	new_line += "\t"
	new_line += title
	rest = line.split (",") [2:len (line)]
	#print (rest)
	for column in rest:
		new_line += "\t"
		new_line += column
	new_lines.append (new_line)

# Write file back out as tsv file instead of csv file
fn = "C:\\data\\m6A_MRM_titles_4_args_punctuated_test.tsv"
with open (fn, 'w') as file:
	file.writelines (new_lines)
print ("DONE !!!\n")