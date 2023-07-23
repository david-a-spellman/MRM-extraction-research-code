file_name = "C:\\data\\titles_with_two_verbs_and_gene_v3.csv"
raw_sentences = list ()
with open (file_name, "r", encoding = "utf8") as file:
	raw_sentences = file.readlines ()
titles = list ()
for s in raw_sentences:
	temp = s.split (",") [1]
	if temp [0] == "\"":
		temp = s.split (",\"") [1]
		temp = temp.split ("\",") [0]
	temp = str (temp.replace ("\"", "") + "\n")
	pm_id = s.split (",") [0]
	#titles.append (str (pm_id + "," + temp))
	titles.append (temp)

file_name = str ("C:\\Users\\David\\Projects\\PretrainingBERT\\training_data\\UnsupervisedTrainingData.txt")
with open (file_name, 'w', encoding = "utf8") as file:
	file.writelines (titles)