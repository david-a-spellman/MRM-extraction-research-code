from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import random

vowels = ['a', 'e', 'i', 'o', 'u', 'y']
# check for a name node on next line if one of these are encountered
category_words = ["protein", "mechanism", "thing", "location"]
# look for op nodes when these are hit
structural_args = ["and"]
# special node types
spec_nodes = ["mod", "name"]
# tokens that are not parsed but should just be jumped over when building the spans
jump_tokens = [",", "the", "and"]
insert_tokens = ["and", "of"]

def normalize_word (word):
	if word == "":
		return word
	if word [-3:len (word)] == "ion" and len (word) > 3:
		word = word [0:-3]
	if word [-3:len (word)] == "ibe" and len (word) > 3:
		word = word [0:-2]
	return word

def normalize_verb (verb):
	if len (verb) < 3:
		return verb
	if verb [-3:len (verb)] == "ies" or verb [-3:len (verb)] == "ing":
		verb = verb [0:-3]
	elif verb [-2:len (verb)] == "ed" or verb [-2:len (verb)] == "es":
		verb = verb [0:-2]
	elif verb [-1] == "y" or verb [-1] == "e":
		verb = verb [0:-1]
	elif verb [-1] == "s" and (not verb [-2] in vowels) and (verb [-2] != "s"):
		verb = verb [0:-1]
	return verb

def varifyTitle (graph, titles):
	for i in range (0, len (graph)):
		if graph [i] in titles:
			return True, i
	return False, 0

def getRegulationVerb (verbs, tokens):
	indicies = list ()
	for verb in verbs:
		for token in tokens:
			if normalize_verb (token).lower () == normalize_verb (verb).lower ():
				indicies.append (tokens.index (token))
	indicies = sorted (indicies)
	for i in range (0, len (indicies)):
		index = indicies [i]
		if (tokens [index] [-2:len (tokens [index])] != "ed") and (tokens [index] [-3:len (tokens [index])] != "ing"):
			return tokens [indicies [i]], indicies
	if len (indicies) == 0:
		print (tokens)
		return None, indicies
	return tokens [indicies [0]], indicies

def find_regulation_verb (graph, title, regulation_verbs, problem_words):
	index_prevs = list ()
	current_verb = 0
	verbs = list ()
	ri = None
	rv = None
	tokens = word_tokenize (title)
	indicies = list ()
	#print (title)
	index = graph.index (title) + 2
	if index >= len (graph):
		#print ("Unexpected AMR structure !!!")
		#print (graph)
		return "", problem_words, (index - 2), None
	#print (graph [index])
	found = False
	while (index < len (graph)):
		regulation_verb = ""
		start = graph [index]
		#print (str ("Searching " + start + " for regulation verb."))
		for c in range (0, len (start)):
			if start [c] == "/":
				#print (start [c])
				found = True
				continue
			elif found and (start [c] != "-" and start [c] != " "):
				regulation_verb += start [c]
				#print (start [c])
			elif found and start [c] == "-":
				#print (start [c])
				found = False
				continue
		if normalize_verb (regulation_verb) in regulation_verbs:
			#print (str (regulation_verb + " is a regulation verb!"))
			index_prevs.append (index)
			issue = True
			for token in tokens:
				if normalize_verb (regulation_verb).lower () in token.lower ():
					regulation_verb = token
					issue = False
			if issue:
				#print ("RV ISSUE !!!")
				#print (regulation_verb)
				index += 1
				continue
			if not regulation_verb in verbs:
				verbs.append ((regulation_verb, tokens.index (regulation_verb)))
				indicies.append (tokens.index (regulation_verb))
			if (verbs [current_verb] [-2:len (regulation_verb)] == "ed" or verbs [current_verb] [-3:len (regulation_verb)] == "ing") and (regulation_verb [-2:len (regulation_verb)] != "ed" or regulation_verb [-3:len (regulation_verb)] != "ing"):
				rv = regulation_verb
				ri = index
				current_verb = verbs.index (rv)
				return rv, problem_words, index, indicies
		elif regulation_verb != "":
			found = False
			#index += 1
			#print (str (regulation_verb + " is not a regulation verb ..."))
			if not regulation_verb in problem_words:
				problem_words.append (str (regulation_verb + "\n"))
		index += 1
	if len (verbs) == 0:
		#print ("No regulation verb is contained in this graph!!!")
		return "", problem_words, index, None
	if rv == None:
		rv = verbs [0] [0]
		ri = verbs [0] [1]
		index = index_prevs [0]
	if rv == verbs [0]:
		indicies = None
		index = index_prevs [0]
	return rv, problem_words, index, indicies

def countPars (line):
	count = 0
	for c in line:
		if c == "(":
			count += 1
		elif c == ")":
			count -= 1
	return count

def transformTokenIndicies (tokens, tok_idx, rv_idx, index, indicies = None):
	tok_idx = sorted (tok_idx)
	#print (tok_idx)
	args = list ()
	# Case where the first form of a regulation verb is clearly the active form of a regulation verb in the title
	if indicies == None:
		# To get first interval before regulation verb
		arg = [str (tok_idx [0]), str (tok_idx [tok_idx.index (rv_idx) - 1]), ""]
		for i in range (int (arg [0]), int (arg [1]) + 1):
			arg [-1] += tokens [i]
			if (i + 1) != (int (arg [1]) + 1):
				arg [-1] += " "
		args.append (arg)
	# Case where regulation verb comes later in the title because of a two verb situation where the first verb has a past tense, and a later verb has the present regulation tense
	else:
		first_idx = tok_idx [tok_idx.index (rv_idx) - 1]
		for i in range (tok_idx.index (first_idx), -1, -1):
			if (first_idx - 1) == tok_idx [i] or (tokens [tok_idx [i]] in jump_tokens and (first_idx - 2) == tok_idx [i - 1]):
				first_idx = tok_idx [i]
		arg = [str (first_idx), str (tok_idx [tok_idx.index (rv_idx) - 1]), ""]
		for i in range (int (arg [0]), int (arg [1]) + 1):
			arg [-1] += tokens [i]
			if (i + 1) != (int (arg [1]) + 1):
				arg [-1] += " "
		args.append (arg)
	args.append ([str (rv_idx), str (rv_idx), tokens [rv_idx]])
	interval = True
	arg = ["0", "0", ""]
	# remove the regulation verb from the token indicies
	start = (tok_idx.index (rv_idx))
	tok_idx.remove (rv_idx)
	for i in range (start, len (tok_idx)):
		"""if len (args) == 3:
			return tokens, args, index, tok_idx"""
		current = tok_idx [i]
		if i < (len (tok_idx) - 1):
			next = tok_idx [i + 1]
		else:
			next = current
		"""if next == rv_idx and interval:
			interval = False
			arg [1] = str (current)
			arg [-1] += tokens [current]
			args.append (arg)
			arg = ["0", "0", ""]
			continue
		elif (next == rv_idx) or (current == rv_idx):
			arg [0] = str (current)
			arg [1] = str (current)
			arg [-1] += tokens [current]
			args.append (arg)
			arg = ["0", "0", ""]
			continue"""
		if (((current + 1) == next) and interval) or (((current + 2) == next) and interval and ((tokens [current + 1]) in jump_tokens)):
			arg [-1] += tokens [current]
			arg [-1] += " "
			continue
		elif (((current + 1) == next)) or (((current + 2) == next) and ((tokens [current + 1]) in jump_tokens)):
			interval = True
			arg [0] = str (current)
			arg [-1] += tokens [current]
			arg [-1] += " "
		elif interval:
			interval = False
			arg [1] = str (current)
			arg [-1] += tokens [current]
			args.append (arg)
			arg = ["0", "0", ""]
		else:
			arg [0] = str (current)
			arg [1] = str (current)
			arg [-1] += tokens [current]
			args.append (arg)
			arg = ["0", "0", ""]
	return tokens, args, index, tok_idx

def getName (line):
	pos1 = 0
	pos2 = 0
	for i in range (0, len (line)):
		if line [i] == "\"":
			pos1 = i
			break
	for i in range ((pos1 + 1), len (line)):
		if line [i] == "\"":
			pos2 = i
			break
	word = ""
	for i in range (pos1 + 1, pos2):
		word += line [i]
	return word

def searchLineForArgs (count, line, word, tok_idx, tokens, graph, index, regulation_verbs):
	count += countPars (line)
	if "/" in line:
		pos = line.index ("/") + 2
	elif "\"" in line:
		#print ("HIT")
		#print (str (int (line.index (" \"") + 2)))
		#print (len (line))
		pos = line.index (" \"") + 2
	else:
		return count, "", tok_idx, line, index
	for i in range (pos, len (line)):
		if line [i] == "\n" or line [i] == ")" or line [i] == "-":
			break
		elif line [i] == " " or line [i] == "\"":
			continue
		word += line [i]
	#if len (word) > 0:
		#print (word)
	# Logic to skip junk tokens in the AMR output that are not tokens in the title
	"""if (word in category_words) and ("name" in graph [index + 1]):
		index += 2
		line = graph [index]
		word = getName (line)"""
	#print (normalize_word (word))
	# To ensure that a word is actually a regulation verb
	"""for verb in regulation_verbs:
		if normalize_verb (word).lower () == normalize_verb (verb).lower ():
			issue = True
			for token in tokens:
				if normalize_verb (word).lower () == normalize_verb (token).lower ():
					issue = False
			if issue:
				for token in tokens:
					if normalize_word (word).lower () in token.lower ():"""
	for token in tokens:
		if normalize_word (word).lower () in token.lower ():
			#print (token)
			if not tokens.index (token) in tok_idx:
				tok_idx.append (tokens.index (token))
				break
	return count, word, tok_idx, line, index

def findArgsAroundRV (rv, rvs, index, graph, title, indicies = None):
	tokens = word_tokenize (title)
	#print (tokens)
	tok_idx = list ()
	count = 0
	index += 1
	line = graph [index]
	while index < len (graph):
		word = ""
		# Add special cases to this if statement as they are encountered in order to ensure that enough lines are processed
		if (not ("/" in line)) and (not ("\"" in line)):
			count = 0
		else:
			#print (line)
			count, word, tok_idx, line, index = searchLineForArgs (count, line, word, tok_idx, tokens, graph, index, rvs)
			#print (count)
		index += 1
		if index < len (graph):
			line = graph [index]
		else:
			break
	rv_idx = None
	"""for token in tokens:
		if normalize_verb (rv.lower ()) in token.lower ():
			rv_idx = tokens.index (token)
			tok_idx.append (rv_idx)"""
	rv, indicies = getRegulationVerb (rvs, tokens)
	if rv == None:
		return tokens, [], index, tok_idx
	rv_idx = tokens.index (rv)
	tok_idx.append (rv_idx)
	#print (tokens)
	#print (rv)
	#print ("ERROR !!!")
	#return tokens, [], 0
	for i in range (0, len (tokens)):
		if not (i in tok_idx):
			if tokens [i] in jump_tokens:
				if ((i - 1) in tok_idx) or ((i + 1) in tok_idx):
					tok_idx.append (i)
	new_tok_idx = list (tok_idx)
	for verb in rvs:
		for idx in tok_idx:
			token = tokens [idx]
			if normalize_verb (token).lower () == normalize_verb (verb).lower ():
				if idx != rv_idx:
					new_tok_idx.remove (idx)
					continue
	tok_idx = new_tok_idx
	for token in tokens:
		if token in insert_tokens:
			temp_idx = tokens.index (token)
			if not temp_idx in tok_idx:
				tok_idx.append (temp_idx)
	return transformTokenIndicies (tokens, tok_idx, rv_idx, index)

# Function for performing positive synonym replacement
def replaceWithSynonym (token, synonym):
	if ((token [-2] == "e") and (token [-1] == "s" or token [-1] == "d")) and synonym [-1] == "e":
		return str (synonym + token [-1])
	else:
		return synonym

exclude_tokens = ["in", "a", "and", "the", "through", "that", "this", "of", "as", "to", "is", "by"]

def getPositive (title):
	tokens = word_tokenize (title)
	new_title = title
	for token in tokens:
		synonyms = list ()
		if (len (wordnet.synsets (token)) == 0) or (token.lower () in exclude_tokens) or token.isnumeric () or len (token) < 3:
			continue
		synset = wordnet.synsets (token.lower ()) [0]
		for word in synset.lemmas ():
			synonyms.append (word.name ())
		for s in synonyms:
			if s in token:
				synonyms.remove (s)
		if len (synonyms) > 0:
			#print (synonyms)
			synonym = None
			i = 0
			i = random.randint (0, len (synonyms) - 1)
			synonym = synonyms [i]
			if '_' in synonym:
				continue
			new_title = new_title.replace (token, replaceWithSynonym (token, synonym))
	return new_title