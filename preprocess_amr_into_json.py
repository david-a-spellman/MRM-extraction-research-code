import json
import io
from OldCreateContrastivePairsVersion import *

file_name = "C:\\Users\\David\\Projects\\CancerKnowledgeGraph\\amr_graph_output_2.txt"
graphs = list ()
with io.open (file_name, 'r', encoding = "utf8") as file:
	line = "\n"
	temp = list ()
	issue = False
	while (line != ""):
		try:
			line = file.readline ()
			if issue and line == "\n":
				temp = list ()
				issue = False
				continue
			elif issue:
				temp.append (line)
				continue
			if len (temp) > 0 and line == "\n":
				graphs.append (temp)
				temp = list ()
				continue
			elif line == "\n":
				continue
			else:
				temp.append (line)
				continue
		except:
			issue = True
			line = "\n"

#print (len (graphs))
#print (graphs [0])
#for line in graphs [0]:
#	print (line)

file_name = "C:\\data\\unsupervised_titles.csv"
titles = list ()
pm_ids = list ()
raw = list ()
with open (file_name, 'r') as file:
	raw = file.readlines ()
for r in raw:
	titles.append (str (r [9:-1] + "\n"))
	pm_ids.append (r [0:7])

# loading in list of regulation verbs
file_name = "C:\\data\\regulation_verbs.csv"
regulation_verbs = list ()
with io.open (file_name, 'r', encoding = "utf8") as file:
	regulation_verbs = file.readlines ()
verbs = list ()
for rv in regulation_verbs:
	rv = rv.replace (",", "")
	rv = rv.replace ("\n", "")
	rv = normalize_verb (rv)
	#print (rv)
	verbs.append (rv.lower ())
regulation_verbs = verbs

# Produce augmented positive title examples
augmented_positives = list ()
j = 0
for title in titles:
	#if j > 10:
	#	quit ()
	#print (title)
	#print (getPositive (title))
	#j += 1
	augmented_positives.append (getPositive (title))

graph_dict = dict ()
problem_titles = list ()
rv_issues = list ()
problem_graphs = list ()
problem_words = list ()
#print (len (graphs))
pairs = list ()
pairs.append ("sent0,sent1,hard_neg\n")
pairs2 = list ()
pairs3 = list ()
for i in range (0, len (graphs)):
#	if i > 5:
#		quit ()
	graph = graphs [i]
	indicies = None
	json_graph = dict ()
	if len (graph) < 3:
		continue
	answer,index = varifyTitle (graph, titles)
	if not (graph [index] in titles):
		continue
	title = titles [titles.index (graph [index])]
	if not answer:
		#print (str ("ISSUE WITH AMR GRAPH AT POSITION " + str (i) + " WITH PM_ID " + str (pm_ids [i])))
		#print (titles [i])
		#print (graph)
		#problem_titles.append (str (pm_ids [i] + "," + titles [i]))
		problem_graphs.append (graph [2])
		continue
	else:
		regulation_verb, problem_words, index, indicies = find_regulation_verb (graph, title, regulation_verbs, problem_words)
		augmented_positive = augmented_positives [titles.index (title)]
		if regulation_verb == "":
			#problem_titles.append (str (pm_ids [i] + "," + titles [i]))
			problem_graphs.append (graph [2])
			continue
		else:
			json_graph [regulation_verb] = dict ()
		#print (title)
		tokens, args, index, tok_idx = findArgsAroundRV (regulation_verb, regulation_verbs, index, graph, title, indicies)
		#for arg in args:
			#print (arg [-1])
		if len (args) == 0:
			rv_issues.append (str (pm_ids [i] + "\n" + titles [i] + "\n\n"))
			continue
		# Check for augmentation issues relating to the regulation verb
		if len (args) < 3:
			print ("ISSUE with AMR!!! skipping graph")
			print (pm_ids [i])
			print (titles [i])
			print (args)
			print (tok_idx)
			continue
		if args [1] [1] in args [0] [1]:
			print (args [0] [1])
		if args [1] [1] in args [2] [1]:
			print (args [2] [1])
		bv = args [0] [-1]
		av = args [2] [-1]
		rv = args [1] [-1]
		rv += " "
		bv = bv.replace (" ,", ",")
		av = av.replace (" ,", ",")
		av = av.replace (rv, "")
		if " in " in bv:
			bv = bv.split (" in ") [0]
		if " in " in av:
			av = av.split (" in ") [0]
		if bv [-1] == ",":
			bv = bv [0:-1]
		if av [-1] == ",":
			av = av [0:-1]
		aug_title = str (title)
		aug_title = aug_title.replace (bv, "&&&")
		aug_title = aug_title.replace (av, "***")
		aug_title = aug_title.replace ("***", bv)
		aug_title = aug_title.replace ("&&&", av)
		pm_id = pm_ids [titles.index (title)]
		a_len = len (av.split (" "))
		b_len = len (bv.split (" "))
		if (a_len > 1) and (b_len > 1):
			#pairs.append (str (pm_id + "\n"))
			title = title.replace ("\n", "")
			aug_title = aug_title.replace ("\n", "")
			augmented_positive = augmented_positive.replace ("\n", "")
			pairs.append (str ("\"" + title + "\",\"" + augmented_positive + "\",\"" + aug_title + "\"\n"))
			#pairs.append (str (aug_title + "\n"))
			#pairs.append (str (bv + "\n"))
			#pairs.append (str (str (args [1] [-1]) + "\n"))
			#pairs.append (str (av + "\n\n"))
		if len (args) < 4:
			continue
		bv = args [0] [-1]
		av = args [-1] [-1]
		bv = bv.replace (" ,", ",")
		av = av.replace (" ,", ",")
		av = av.replace (rv, "")
		if " in " in bv:
			bv = bv.split (" in ") [0]
		if " in " in av:
			av = av.split (" in ") [1]
		if bv [-1] == ",":
			bv = bv [0:-1]
		if av [-1] == "," or av [-1] == ".":
			av = av [0:-1]
		aug_title = str (title)
		aug_title = aug_title.replace (bv, "&&&")
		aug_title = aug_title.replace (av, "***")
		aug_title = aug_title.replace ("***", bv)
		aug_title = aug_title.replace ("&&&", av)
		#pm_id = pm_ids [titles.index (title)]
		a_len = len (av.split (" "))
		b_len = len (bv.split (" "))
		if (a_len > 1) and (b_len > 1):
			pairs2.append (str (pm_id + "\n"))
			pairs2.append (str (title))
			pairs2.append (str (aug_title + "\n"))
			pairs2.append (str (bv + "\n"))
			pairs2.append (str (av + "\n\n"))
		bv = args [-2] [-1]
		av = args [-1] [-1]
		bv = bv.replace (" ,", ",")
		av = av.replace (" ,", ",")
		av = av.replace (rv, "")
		bv = bv.replace (rv, "")
		if " in " in bv:
			bv = bv.split (" in ") [0]
		if " in " in av:
			av = av.split (" in ") [1]
		if bv [-1] == ",":
			bv = bv [0:-1]
		if av [-1] == "," or av [-1] == ".":
			av = av [0:-1]
		aug_title = str (title)
		aug_title = aug_title.replace (bv, "&&&")
		aug_title = aug_title.replace (av, "***")
		aug_title = aug_title.replace ("***", bv)
		aug_title = aug_title.replace ("&&&", av)
		#pm_id = pm_ids [titles.index (title)]
		a_len = len (av.split (" "))
		b_len = len (bv.split (" "))
		if (a_len > 1) and (b_len > 1):
			pairs3.append (str (pm_id + "\n"))
			pairs3.append (str (title))
			pairs3.append (str (aug_title + "\n"))
			pairs3.append (str (bv + "\n"))
			pairs3.append (str (av + "\n\n"))
		
print (len (graphs))
file_name = "C:\\data\\pairs_1_full.csv"
with open (file_name, 'w') as file:
	file.writelines (pairs)

"""
file_name = "C:\\data\\pairs_2_full.txt"
with open (file_name, 'w') as file:
	file.writelines (pairs2)


file_name = "C:\\data\\pairs_3_full.txt"
with open (file_name, 'w') as file:
	file.writelines (pairs3)
"""

file_name = "C:\\data\\RV_issues.txt"
with open (file_name, 'w') as file:
	file.writelines (rv_issues)


"""
# Write problematic titles to file
file_name = "C:\\data\\unsupervised_problem_titles.csv"
with open (file_name, 'w') as file:
	file.writelines (problem_titles)
"""

# Write problematic graphs to file
file_name = "C:\\data\\problem_AMR_graphs.txt"
with io.open (file_name, 'w', encoding = "utf8") as file:
	file.writelines (problem_graphs)

# Write problematic words to file
file_name = "C:\\data\\check_for_RVs.txt"
with io.open (file_name, 'w', encoding = "utf8") as file:
	file.writelines (problem_words)

print ("DONE !!!")