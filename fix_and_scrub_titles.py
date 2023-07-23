def fix_and_scrub_titles (original, final, output):
	# open and read lines from both versions
	original_titles = list ()
	final_titles = list ()
	output_titles = list ()
	with open (original, 'r') as orgf:
		original_titles = orgf.readlines ()
		print (len (original_titles))
	with open (final, 'r') as finf:
		final_titles = finf.readlines ()
		print (len (final_titles))
	# Remove all punctuation and quotes from original csv save the commas
	for i in range (0, len (original_titles)):
		original_titles [i] = original_titles [i].replace (":", "")
		original_titles [i] = original_titles [i].replace (".", "")
		original_titles [i] = original_titles [i].replace (";", "")
		# Remove all collumns save the collumns containing the title
		if ("\"" in original_titles [i] and original_titles [i] [9] == "\""):
			title = original_titles [i].split ("\"") [1].replace (",", "")
		else:
			title = original_titles [i].split (",") [1]
		# Now add back in PMID and new line character
		original_titles [i] = str (original_titles [i].split (",") [0] + "," + title)
	for item in original_titles:
		print (item)
	# Now fix the titles in the version with newest labeling by matching rows using the PMID
	for i in range (0, len (final_titles)):
		ft = ""
		pm_id = final_titles [i].split (",") [0]
		for j in range (0, len (original_titles)):
			if (pm_id == original_titles [j].split (",") [0]):
				ft = final_titles [i].split (",")
				ft [1] = original_titles [j].split (",") [1]
				#print (ft)
		ft_string = ""
		for item in ft:
			if not (item == "\n," or item == ",\n" or item == "\n" or item == ","):
				ft_string += str (item + ",")
		ft_string = ft_string.replace ("\n,", "")
		ft_string = ft_string.replace ("\n", "")
		ft_string += "\n"
		output_titles.append (ft_string)
	#for item in output_titles:
		#print (item)
	with open (output, "w") as out_file:
		out_file.writelines (output_titles)

original = "C:\\data\\auto_generated_events.csv"
final = "C:\\data\\DSpellman Labelled Sorted Cleaned July5.csv"
output = "C:\\data\\CleanedLabelingOfPMTitles.csv"
fix_and_scrub_titles (original, final, output)