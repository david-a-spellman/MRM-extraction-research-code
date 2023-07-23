"""
Post processing functions to help correct arguments and add any critical missing context into the spans
Also includes functions to help extract the correct regulation verbs once the correct argument spans are identified
Each function takes a list of tokens as the title and a dictionary with the argument names as the keys and the spans as the values
Each span is a list object
"""

junk_tokens = ["the", "to", "is", "by", "via", "through", "for"]

# Function to see if one list of strings intersects with the other
# If any elements in one list are in the other it will return 'True'
def intersects (l1, l2):
	result = False
	for item in l1:
		if item in l2:
			result = True
	return result

# function to see if the span is between two tokens
# returns True if yes and False if no
def spanBetween (token1, token2, span):
	if int (span [0]) > int (token1) and int (span [1]) < int (token2):
		return True
	else:
		return False

# returns True if any span in the list is between the two tokens
def anySpanBetween (token1, token2, span_list):
	result = False
	for span in span_list:
		if spanBetween (token1, token2, span):
			result = True
			break
	return result

# helper function returns whether two spans overlap or not
# returns True if they overlap and False if they are disjoint
# Each span should be a list of length 2
def spans_overlap (span1, span2):
	if int (span1 [1]) < int (span2 [0]):
		return False
	elif int (span1 [0]) > int (span2 [1]):
		return False
	else:
		return True

# Performs span_overlap but is checking to see if span1 overlaps with any spans in span_list
# If span1 overlaps with one span in span_list True is returned, otherwise False is returned
def anySpansOverlap (span1, span_list):
	result = False
	for span in span_list:
		if spans_overlap (span1, span):
			result = True
			break
	return result

# tests to see if span2 comes between span1 and a token that comes before it
# The token should be a single int as an index into the title
# Returns True if so or False otherwise
def comesBeforeSpanAfterToken (span1, span2, token):
	if (int (span1 [0]) > int (span2 [1])) and int (token) < int (span2 [0]):
		return True
	else:
		return False

# Returns True if any of the spans in span_list are between span1 and the token with the token index coming before span1
def anyComesBeforeSpanAfterToken (span1, span_list, token):
	result = False
	for span in span_list:
		if comesBeforeSpanAfterToken (span1, span, token):
			result = True
			break
	return result

# tests to see if span2 comes between span1 and a token that comes after it
# The token should be a single int as an index into the title
# Returns True if so or False otherwise
def comesAfterSpanBeforeToken (span1, span2, token):
	if (int (span1 [1]) < int (span2 [0])) and int (token) > int (span2 [1]):
		return True
	else:
		return False

# Returns True if any of the spans in span_list are between span1 and the token with the token index coming after span1
def anyComesAfterSpanBeforeToken (span1, span_list, token):
	result = False
	for span in span_list:
		if comesAfterSpanBeforeToken (span1, span, token):
			result = True
			break
	return result

# function to read in file with potential regulation related trigger verbs and produce a list of their possible tenses to be found in titles
# All verbs and their tenses will be fully in lower case
# When dealing with the tokens in the titles they should also be converted to lower case before being compared with the list returned by this function
def readRegulationVerbs (file_name):
	verb_strings = list ()
	with open (file_name, 'r') as reading:
		verb_strings = reading.readlines ()
	for i in range (0, len (verb_strings)):
		verb_strings [i] = verb_strings [i].replace ('\n', '')
		verb_strings [i] = verb_strings [i].replace (',', '')
	full_list = list ()
	for verb in verb_strings:
		if verb [-1] == 'e':
			full_list.append (verb.lower ())
			full_list.append (str (verb [0:len (verb) - 1] + "ing").lower ())
			full_list.append (str (verb + 's').lower ())
			full_list.append (str (verb + 'd').lower ())
	#		full_list.append (lower (str (verb [0:len (verb) - 1] + "ion")))
		elif verb [-1] == 's':
			full_list.append (verb.lower ())
			full_list.append (str (verb + 's').lower ())
			full_list.append (str (verb + "ing").lower ())
		else:
			full_list.append (verb.lower ())
			full_list.append (str (verb + "ing").lower ())
		if verb [-1] == 'y':
			full_list.append (str (verb [0:len (verb) - 1] + "ied").lower ())
			full_list.append (str (verb + "ies").lower ())
		else:
			full_list.append (str (verb + 'ed').lower ())
			full_list.append (str (verb + 's').lower ())
	return full_list

# For all of these functions the title argument should contain all lower case strings that have been processed by lower for easy comparison
# For some arguments such as argument1 duplicate predictions need to be dealt with
def fixArg1 (title, arg_dict, verbs):
	arg1 = arg_dict ["initiator"]
	arg2 = arg_dict ["process"]
	arg3 = arg_dict ["location"]
	arg5 = arg_dict ["target"]
	
def fixArg2 (title, arg_dict, verbs):
	other_args = list ()
	if "initiator" in arg_dict:
		arg1 = arg_dict ["initiator"]
		other_args.append (arg1)
	if "process" in arg_dict:
		arg2 = arg_dict ["process"]
	else:
		return arg_dict
	if "location" in arg_dict:
		arg3 = arg_dict ["location"]
		other_args.append (arg3)
	else:
		arg3 = None
		arg_dict ["location"] = None
	if "target" in arg_dict:
		arg5 = arg_dict ["target"]
		other_args.append (arg5)
	old_trigger = arg_dict ["trigger"]
	new_trigger = old_trigger
	triggers = list ()
	#print (str (arg2))
	change = False
	if not anySpansOverlap (arg2, other_args):
		# Logic to capture rest of argument 2 span if some tokens are left out that are between the nearest trigger and the span for argument 2
		for verb in verbs:
			if (verb in title) and (not anyComesBeforeSpanAfterToken (arg2, other_args, title.index (verb))):
				change = True
				triggers.append (title.index (verb))
		if len (triggers) > 1:
			trig = triggers [0]
			for trigger in triggers:
				if int (trigger) < int (arg2 [0]) and int (trigger) > int (trig):
					trig = trigger
			new_trigger = str (trig)
		elif len (triggers) == 1:
			new_trigger = str (triggers [0])
		if change:
			for i in range (int (new_trigger) + 1, int (arg2 [0])):
				if not title [i] in junk_tokens:
					arg2 [0] = str (i)
					break
		elif ("location" in arg_dict) and arg_dict ["location"] != None:
			if (not anySpanBetween (arg3 [1], arg2 [0], other_args)) and int (new_trigger) == (int (arg3 [0]) - 1):
				arg2 [0] = str (int (arg3 [1]) + 1)
		# Case to capture rest of span for argument 2 if there are tokens between the span and argument 3 that are missed
		if ('in' in title) and (int (new_trigger) + 1) == int (arg2 [0]):
			index = title.index ("in")
			if not anyComesAfterSpanBeforeToken (arg2, other_args, index):
				arg2 [1] = str (index - 1)
		# Case to deal with mis-match trigger and process, the trigger will be changed to be the correct trigger for the process
		if (int (arg2 [0]) - int (new_trigger)) > 2 and (title [int (arg2 [0]) - 1] in junk_tokens):
			for verb in verbs:
				if (verb in title) and (int (arg2 [0]) - title.index (verb)) <= 2:
					new_trigger = str (title.index (verb))
	# Case where args 2 and 3 are same
	# In this case set location to 'None' and remove it from the arg dict
	elif arg2 == arg3:
		arg3 = None
		del arg_dict ["location"]
	else:
		change = True
		temp = [int (arg2 [0]), int (arg2 [1]), int (arg3 [0]), int (arg3 [1])]
		end = 0
		start = len (title)
		for item in temp:
			if item > end:
				end = item
			if item < start:
				start = item
		for token in junk_tokens:
			if token in title [start : (end + 1)]:
				change = False
		if change:
			dif_arg2 = int (arg2 [1]) - int (arg2 [0])
			dif_arg3 = int (arg3 [1]) - int (arg3 [0])
			s_a2 = int (arg2 [0])
			s_a3 = int (arg3 [0])
			e_a2 = int (arg2 [1])
			e_a3 = int (arg3 [1])
			# Case to handle if arg2 comes directly after arg3 and the predicted spans overlap
			if dif_arg2 > dif_arg3 and e_a2 > e_a3:
				arg2 [0] = str (int (arg3 [1]) + 1)
			elif dif_arg2 < dif_arg3 and s_a2 < s_a3:
				arg3 [1] = str (int (arg2 [0]) - 1)
	# Case where there is no arg3 when there should be and instead arg3 was predicted as part of arg2's span
	# split the arguments apart using the word "cell"
	# Have not yet found an example where a junk token can be used to partition such a mis-classified span
	arg2_span = title [int (arg2 [0]) : int (arg2 [1])]
	if arg_dict ["location"] == None and "cell" in arg2_span:
		index = title.index ("cell")
		if index > int (arg2 [0]) and index < int (arg2 [1]):
			arg3 = [arg2 [0], str (index)]
			arg2 [0] = str (index + 1)
	# case that a single legal token is left out between argument2 and the trigger
	include = ["cell", "cells"]
	if arg3 != None:
		if (int (arg2 [0]) - 1) == (int (new_trigger) + 1) and int (arg3 [0]) > int (arg2 [1]) and not (title [int (new_trigger) + 1] in junk_tokens):
			arg2 [0] = str (int (new_trigger) + 1)
	# Case where there is no predicted argument 3 and multiple legal tokens exists between trigger and argument 2, meaning part of argument 2 that comes directly after the token has not been predicted
	if arg3 == None and int (arg2 [0]) > int (new_trigger):
		segment = title [int (new_trigger) + 1: int (arg2 [0])]
		add = False
		for item in segment:
			if item in include:
				add = True
		for item in segment:
			if item in junk_tokens:
				add = False
		if add:
			arg2 [0] = str (int (new_trigger) + 1)
	# Case where a second trigger is contained in the prediction for argument2
	# remove anything past the second trigger along with any remaining junk tokens
	segment = title [int (arg2 [0]): int (arg2 [1]) + 1]
	if intersects (segment, verbs) and int (arg2 [0]) > int (new_trigger):
		# case where it is another form of regulation being anded to the original in a compound statement
		# simply remove the "and" and everything that comes after in argument 2
		if "and" in segment:
			index = segment.index ("and")
			index += 1
			index += int (new_trigger)
			arg2 [1] = str (index)
	# Case where the process is specifically modifying some entity that is not the location, but that is not include will drop context
	# Follows the form argument2 "of" entity "in" argument3
	# But the prediction does not include "of" entity
	# For this case check to see that the "of" and "in" tokens are in the right places
	if arg3 != None:
		v2 = int (arg2 [1])
		v3 = int (arg3 [0])
		if v3 > v2:
			ct1 = title [v3 - 1]
			ct2 = title [v2 + 1]
			if ct1 == "in" and ct2 == "of":
				arg2 [1] = str (v3 - 2)
	# Take care of case where there is no arg3, but there is an arg5, and not all of the right side of the arg2 span is predicted past the token "with"
	# In this case argument2 should be extended to include everything to the right of the current prediction starting with "with" and ending before "through" or "by" or "via" for arg5
	if arg2 != arg_dict ["process"]:
		arg_dict ["process"] = arg2
	if arg3 != arg_dict ["location"]:
		arg_dict ["location"] = arg3
	arg_dict ["trigger"] = new_trigger
	if arg_dict ["location"] == None:
		del arg_dict ["location"]
	return arg_dict