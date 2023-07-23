import json

file_name = "C:\\users\\david\\projects\\temp_gen\\data\\muc34\\proc_output\\ree_test.json"
test_json = dict ()
with open (file_name, 'r') as reading:
	test_json = json.load (reading)
print ("test data points: " + str (len (test_json)))
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\muc34\\proc_output\\ree_train.json"
train_json = dict ()
with open (file_name, 'r') as reading:
	train_json = json.load (reading)
print ("train data points: " + str (len (train_json)))
file_name = "C:\\users\\david\\projects\\temp_gen\\data\\muc34\\proc_output\\ree_dev.json"
dev_json = dict ()
with open (file_name, 'r') as reading:
	dev_json = json.load (reading)
print ("dev data points: " + str (len (dev_json)))
print ("DONE!")