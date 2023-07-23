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
#	print (temp)
"""
i = 1
for t in titles:
	file_name = str ("C:\\Users\\David\\Projects\\PretrainingBERT\\training_data\\" + str (i) + ".txt")
	with open (file_name, 'w', encoding = "utf8") as file:
		file.write (t)
		i += 1
print ("DONE !!!")
"""


import amrlib
import spacy

amrlib.setup_spacy_extension()
nlp = spacy.load ("C:\\Users\\David\\Projects\\CancerKnowledgeGraph\\en_core_sci_md\\en_core_sci_md-0.5.1\\en_core_sci_md\\en_core_sci_md-0.5.1\\")
i = 0
for title in titles:
	if i < 2253:
		i += 1
		continue
	sentence = nlp (title)
	for span in sentence.sents:
		graphs = span._.to_amr ()
		print (span.text.encode("utf-8"))
		for s in graphs:
			print (s.encode('utf-8', 'ignore'))
	i += 1