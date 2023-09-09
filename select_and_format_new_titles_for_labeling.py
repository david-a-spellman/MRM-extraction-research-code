# Selecting 400 new titles through active learning strategy
import os

new_title_count = 400
in_file = "C:\\data\\dataset_2_predictions.csv"
title_file = "C:\\data\\unsupervised_titles_utf8.csv"
intermediate_file = "C:\\data\\new_400_chosen_titles.csv"
out_file = "C:\\data\\new_400_weakest_titles.tsv"

command1 = str ("Python .\\select_new_titles_to_label.py " + in_file + " " + str (new_title_count) + " " + intermediate_file)
command2 = str ("Python .\\reformat_new_titles_for_labeling.py " + intermediate_file + " " + title_file + " " + out_file)

# Running commands
print ("Running first title selection process!")
os.system (command1)
print ("Done with title selection process! Now running title reformatting process!")
os.system (command2)
print (str ("Titles have been reformatted and written back out to file as: " + out_file))
print ("DONE !!!")