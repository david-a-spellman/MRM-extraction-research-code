import sys

# Converting from CSV to TSV
# Will also replace titles without commas with fully punctuated original version
# Will remove the logit scores

in_file = sys.argv [1]
title_file = sys.argv [2]
out_file = sys.argv [3]

# Load the inputs and the original titles
with open (in_file, 'r') as file:
	lines = file.readlines ()
# The title file should be specified as utf8
with open (title_file, 'r', encoding = "utf8") as file:
	titles = file.readlines ()
# remove the newlines on the punctuated titles
new_titles = list ()
for title in titles:
	new_titles.append (title.replace ("\n", ""))
titles = new_titles

assert len (titles) >= (len (lines) - 1), "The number of titles selected must be less than or equal to the total pool of titles!"
count = len (lines) - 1

# Generator for getting the samples for labeling and their corresponding original fully punctuated title
def get_title (lines, titles):
	count = 0
	for line in lines:
		pmid = line [0 : 8]
		count += 1
		for title in titles:
			if pmid in title:
				items = list ()
				items.append (pmid)
				items.append (title [9 : -1])
				args = line.split (",") [-10 : -5]
				for arg in args:
					items.append (arg)
				yield items
			else:
				continue
	print (count)

# Get outputs
header_parts = lines [0].split (",")
header = ""
for part in header_parts [0 : 7]:
	header += part
	if part != header_parts [6]:
		header += "\t"
header += "\n"
lines = lines [1:]
outputs = list ()
outputs.append (header)
itterator = get_title (lines, titles)
print (count)
for i in range (count):
	out_string = ""
	items = next (itterator)
	for j in range (len (items)):
		item = items [j]
		out_string += item
		if j < (len (items) - 1):
			out_string += "\t"
		else:
			out_string += "\n"
	outputs.append (out_string)

# Write the outputs out to the out_file
with open (out_file, 'w', encoding = "utf8") as file:
	file.writelines (outputs)
print (str ("Wrote reformated titles out to " + out_file))
print ("DONE !!!")