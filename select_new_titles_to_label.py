import sys
from math import *

# This file takes a csv or tsv file to search as first commandline input
in_file = sys.argv [1]
extension = in_file.split ('.') [-1]
new_title_count = sys.argv [2]
out_name = sys.argv [3]

with open (in_file, 'r') as file:
	lines = file.readlines ()
titles = list ()
i = 0
for line in lines:
	if i > 0:
		titles.append (line.replace ("\n", ""))
	i += 1

# Produces a score that indicates how much the model struggled on the particular title
# The higher the score the more trouble
def score_title (title, extension):
	arguments = list ()
	score = 0
	if extension == "csv":
		arguments = title.split (',')
	else:
		pass
	arg1_logit = arguments [-5]
	arg2_logit = arguments [-4]
	arg3_logit = arguments [-3]
	arg4_logit = arguments [-2]
	rv_logit = arguments [-1]
	try:
		if arg1_logit == "":
			score += 20
		else:
			score += (10 - float (arg1_logit))
		if arg2_logit == "":
			score += 20
		else:
			score += (10 - float (arg2_logit))
		if rv_logit == "":
			score += 30
		else:
			score += (10 - float (rv_logit))
		if arg3_logit == "":
			score += 0
		else:
			score += (20 - float (arg3_logit))
		if arg4_logit == "":
			score += 0
		else:
			score += (30 - float (arg4_logit))
	except:
		print ("Issue converting an argument of title to float, where the arguments are:")
		for arg in arguments [-5:]:
			print (arg)
		print ("The full title line in data file:")
		print (title)
	return score

# Generator function for itterating over the titles and there indicies
def get_titles (titles):
	for title in titles:
		index = titles.index (title)
		yield (title, index)

# Function for performing murdge sort on the score tuples
# Sorts from highest to lowest score
def murdge_sort_tuples (scores):
	length = len (scores)
	if length == 0:
		return []
	if length == 1:
		return [scores [0]]
	middle = ceil (length / 2) - 1
	try:
		pivit = scores [middle] [0]
		print (pivit)
	except:
		print ("ISSUE WITH OBTAINING VALUE FOR PIVIT")
		print (len (scores))
		print (middle)
		print (str (scores [middle]))
		quit ()
	i = 0
	while i < middle:
		item = scores [i]
		if item [0] < pivit:
			temp = item
			scores.pop (i)
			middle -= 1
			scores.append (temp)
		else:
			i += 1
	i = (middle + 1)
	while i < len (scores):
		item = scores [i]
		if item [0] > pivit:
			temp = item
			scores.pop (i)
			scores.insert (0, temp)
			middle += 1
		else:
			i += 1
	left = scores [0 : middle + 1]
	right = scores [middle + 1:]
	sorted_left = murdge_sort_tuples (left)
	sorted_right = murdge_sort_tuples (right)
	for item in sorted_right:
		sorted_left.append (item)
	return sorted_left

# Build up list of tuples, where each tuple is a score followed by the index of the corresponding title
scores = list ()
itterator = get_titles (titles)
for i in range (len (titles)):
	title, index = next (itterator)
	scores.append ((score_title (title, extension), index))

# sort scores using murdge sort
print (scores [:10])
scores = murdge_sort_tuples (scores)
print (scores [:10])

# Take how many new titles for annotation are desired
new_titles = list ()
new_titles.append (lines [0])
for i in range (int (new_title_count)):
	index = scores [i] [-1]
	new_titles.append (str (titles [index]) + "\n")
#for new_title in new_titles [:5]:
#	print (new_title)

# Write chosen titles out to file
out_file = str (out_name)
with open (out_file, 'w') as file:
	file.writelines (new_titles)
print (str ("Wrote selected titles out to " + out_file))
print ("DONE !!!")