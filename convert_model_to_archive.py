paramsTest = prms.Params.from_file("/mnt/c/Users/David/Projects/SimCSE/pubmedbert/config.json")
import allennlp.models.model as mdl
myModel = mdl.Model.load (paramsTest, "./pubmedbert", weights_file = "pytorch_model.bin")