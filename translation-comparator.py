# compare-translations.py
# input: 3+ translations
# function: 
# -deconstruct comparable sentences into similar parts. 
# -Iso differences and vote. 
# output: concepts in sentence
# example: 
# All armies prefer high ground to low and sunny places to dark. 
# 1: All armies
# 2: prefer
# 3: high ground
# 4: to
# 5: low
# 6: and
# 7: sunny places
# 8: to
# 9: dark
# data: knowledge of which words are which part of speech. if I can do it manually, then a program can do it better.

import re
from tabulate import tabulate

# === Global Variables ===

exclude_exception_words = True # we need to pass thru all positions once wo exception words bc they only represent valid matches after all other words have been matched to completion



#p1-1
init_sentence_v1 = "The art of war is of vital importance to the state." 
init_sentence_v2 = "War is a matter of vital importance to the state."
init_sentence_v3 = "Strategy is the great work of the organization." 

print("\n===Initial Sentences===\n")
init_sentences = [init_sentence_v1, init_sentence_v2, init_sentence_v3]

# print version names
version_names = ["Giles", "Griffith", "Wing"] # Giles, Griffith, Wing
version_names_string = ''
for vn in version_names:
	version_names_string += vn + "\t" 
print(version_names_string)

init_sentences_string = ''
for sentence in init_sentences:
	init_sentences_string += sentence + "\t" 
print(init_sentences_string)

print()
	
# deconstruct sentences into lists of words
print("\n===Deconstruct Strings===\n")
all_sentences_words = [] # = [['the','art','of','war','is'],['war','is'],['strategy','is']]
for init_sentence in init_sentences:
	init_sentence = init_sentence.lower()
	
	words = re.split("\s", init_sentence)
	print("words: " + str(words))
	all_sentences_words.append(words)
print("\nall_sentences_words: " + str(all_sentences_words) + "\n")

print()

print("\n===Initial Positions===\n")
all_positions_words = [all_sentences_words]
print("all_positions_words: " + str(all_positions_words))

def find_match(focus_word, exception_words):
	match = False
	for ex_word in exception_words:
		# use exception words as separators only after other options exhausted
		if ex_word == focus_word:
			print("EXCEPTION WORD\n")
			match = True
			break
	return match
	
# check if either focus or compare word is at idx 0 while other is not
def check_context(focus_word_idx, compare_word_idx):
	print("\n===Check Context===\n")
	
	in_context = True
	
	if focus_word_idx == 0 and compare_word_idx != 0:
		in_context = False
	elif compare_word_idx == 0 and focus_word_idx != 0:
		in_context = False

	return in_context

def isolate_positions(all_positions_words, exclude_exception_words=True):
	print("\n===Isolate All Positions===\n")

	# we do not know how many positions there will be at the end so loop until positions taken as far as possible
	position_idx = 0
	while position_idx < len(all_positions_words): # all_positions_words increases in size when new position isolated

		print("\n===Isolate/Separate Positions " + str(position_idx) + " and " + str(position_idx+1) + "===\n")

		position = all_positions_words[position_idx]
		print("position " + str(position_idx) + ": " + str(position))
	
		next_position = []
	
		# we specify focus version bc we also have compare version
		for focus_version_idx in range(len(position)):
			print("focus_version_idx: " + str(focus_version_idx))
		
			focus_version = position[focus_version_idx]
			print("focus_version: " + str(focus_version))
		
			for compare_version_idx in range(len(position)):
				print("compare_version_idx: " + str(compare_version_idx))
			
				# do not compare if same as focus sentence
				if compare_version_idx != focus_version_idx:
				
					compare_version = position[compare_version_idx]
					print("compare_version: " + str(compare_version))
				
					for focus_word_idx in range(len(focus_version)):
				
						focus_word = focus_version[focus_word_idx]
						print("focus_word: " + focus_word)
											
						for compare_word_idx in range(len(compare_version)):
					
							compare_word = compare_version[compare_word_idx]
							print("compare_word: " + compare_word)
						
							if focus_word == compare_word:
								print("MATCH: " + focus_word + " == " + compare_word)
							
								exception_words = ["the","of"]
							
								in_context = True # naively true bc check negates it
							
								focus_version_end_match_idx = focus_word_idx
							
								if exclude_exception_words: # frame variable exclude bc first condition is positive. could frame variable as include bc we take special action if include. it is normal to exclude exception words so does not inherently require check. 
									print("exclude exception words")
									
									if find_match(focus_word, exception_words):
										# we know this word is an exception word and we are excluding exception words, 
										# so continue to next focus word by breaking out of compare word loop
										break
										
								else: # include exception words
									# if we find a matching exception word, and we are including exception words, we need to reorganize positions 
									# so keep all prior positions and compress all following positions into current position? no. insert and shift positions.
									
									# if we find a match with exception word or multiple occurrences, 
									# then check context
									if find_match(focus_word, exception_words):
									
										#in_context = check_context(focus_word_idx, compare_word_idx)
										if focus_word_idx == 0 and compare_word_idx != 0:
											break
										elif compare_word_idx == 0 and focus_word_idx != 0:
											# we know this word is not in context 
											# bc it is exception word AND either focus word or compare word is at idx 0 but other is not
											# so break out of compare words to next focus word
											# or if multiple occurrences in compare version then go to next instance in compare version
											
											# we know it is out of context but there might be another compare instance
											if compare_version.count(focus_word) == 1: # compare_word always = focus_word here
												print("only one instance of focus_word in compare_version!")
												break
											# else if there are multiple instances check them for pattern match
											else:
												continue
											
												
										if focus_word == "of":
											# check if 'of' followed by 'the'
											next_focus_word = focus_version[focus_word_idx+1]
											if next_focus_word == 'the' and next_compare_word != 'the':
												# change the pattern end idx to after 'the'
												if focus_word_idx == 0 and compare_word_idx != 0:
													print("focus_word is at start but compare word is not!")
													break
												else:
													focus_version_end_match_idx += 1
													break
											else:
												break
										elif focus_word == "the":
											if focus_word_idx == 0:
												break
												
								# check for multiple instances
								if focus_version.count(focus_word) > 1:
									print("multiple instances of \'" + focus_word + "\'")	
								
									if focus_word_idx == 0 and compare_word_idx != 0:
										break
									elif compare_word_idx == 0 and focus_word_idx != 0:
										if compare_version.count(focus_word) == 1:
											break
										else:
											continue
									# check if the following word after either occurence matches the compare sentence and if so we know which instance it is
									else:
										# check if next focus word matches parallel/next compare word
										next_focus_word = next_compare_word = ''
										if len(focus_version) > focus_word_idx+1:
											next_focus_word = focus_version[focus_word_idx+1]
										if len(compare_version) > compare_word_idx+1:
											next_compare_word = compare_version[compare_word_idx+1]
										print("next_focus_word: " + next_focus_word)
										print("next_compare_word: " + next_compare_word)
								
										pattern_match = True
										
										if next_focus_word != next_compare_word:
											# then if not, check next occurence
											
											for word_idx in range(focus_word_idx,len(focus_version)):
												word = focus_version[word_idx]
												if word == focus_word:
													# check next word
													next_focus_word = focus_version[word_idx+1]
										
													if next_focus_word == next_compare_word: # we know next instance of focus word is pattern match but current instance of focus word is not a pattern match so go to next focus word
														pattern_match = False
														break
												
											if not pattern_match:
												break			
							
								# made sure valid match before splitting
								# create the split
								# split before and after end of pattern match
								focus_version_updated_position = focus_version[:focus_version_end_match_idx+1]
								print("focus_version_updated_position: " + str(focus_version_updated_position))
								focus_version_new_position = focus_version[focus_version_end_match_idx+1:]
								print("focus_version_new_position: " + str(focus_version_new_position))
							
								# init new list for new position here now that we know we need another position 
								# so we can access each idx
								# but only do this the first instance of new position
								if len(next_position) == 0:
									for idx in range(len(position)):
										next_position.append([])
							
								position[focus_version_idx] = focus_version_updated_position # updated p0
								print("position: " + str(position))
								next_position[focus_version_idx] = focus_version_new_position # new p1
								print("next_position: " + str(next_position))
			
				print()
			
			print()
		
		# insert/organize positions
		
		all_positions_words[position_idx] = position
		print("all_positions_words: " + str(all_positions_words))
	
		# only increase the size of all_positions if if next_position is not empty
		print("next_position: " + str(next_position))
		if len(next_position) > 0:
			if len(next_position[0]) > 0:
				print("we have a next position so add it to all positions")
				# check if it should be appended or inserted. can always be inserted bc works for both cases if last or middle element
				all_positions_words.insert(position_idx + 1, next_position) #formerly all_positions_words.append(next_position)
				print("all_positions_words: " + str(all_positions_words))
	
		# by the time it reaches this point exactly one position has been added
		# bc after adding position we break and loop to the next position
		position_idx += 1
		

		
isolate_positions(all_positions_words)

exclude_exception_words = False

isolate_positions(all_positions_words, exclude_exception_words)
	
	
print("\n===Final Positions===\n")

print("\n===Reconstruct Strings===\n")

all_positions = []
for all_position_y_words in all_positions_words:
	py_strings = []
	for version_x_position_y_words in all_position_y_words:
		vx_py_string = ' '.join([str(item) for item in version_x_position_y_words])
		py_strings.append(vx_py_string)
	all_positions.append(py_strings)
print("all_positions: " + str(all_positions))

# print version names, set after init sentences
print(version_names_string)
table = [version_names]

# print all versions of all positions
for position in all_positions:
	p_versions_string = ''
	for v in position:
		#print("version: " + v)
		p_versions_string += v + "\t" 
	print(p_versions_string)
	table.append(position)
	


print(tabulate(table))