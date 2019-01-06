"""
	Utility module comprised of static functions to operate
	on word files, lists and strings
"""

"""
	Returns:
		Pair of words with greatest length product -
			1) where word1 and word2 are not same;
			2) word1 and word2 do not share common characters
		(see requirements.txt file)
"""
def get_highest_scoring_pair(sorted_list1, sorted_list2, count):
	# compare words against each other using 2 dupe lists
	curr_max = 0
	curr_val = 0
	for idx1 in range(0, count, 1):
		w1 = sorted_list1[idx1]
		for idx2 in range(0, count, 1):
			w2 = sorted_list2[idx2]

			# exclude comparing words a/g self and words sharing common characters
			duplicate_word = _is_duplicate(w1, w2)
			shared_chars_between_words = _shares_common_chars(w1, w2)

			# debugging conditional/print stmnts
			'''
			if duplicate_word or shared_chars_between_words:
				if duplicate_word:
					print 'word1={w1} || word2={w2}: DUPLICATE_WORD'.format(w1=w1, w2=w2)
				if shared_chars_between_words:
					print 'word1={w1} || word2={w2}: WORD_SHARE_COMMON_CHARS'.format(w1=w1, w2=w2)
			'''
			if not (duplicate_word) and not (shared_chars_between_words):
				'''
				print 'word1={w1} || word2={w2}: NOT_DUPE_OR_SHARED_CHARS - prev_max={prev}; curr_score={' \
					  'score}'.format(
					w1=w1,
					w2=w2,
					prev=curr_max,
					score=_get_pair_score(
						w1,
						w2))
				'''


				if curr_max < 1:
					curr_max = _get_pair_score(w1, w2)
				else:
					curr_val = _get_pair_score(w1, w2)

				#print 'Highest scoring word pair: {w1} {w2} - score={score}'.format(w1=w1, w2=w2,score=_get_pair_score(w1, w2))

		# return first score > 0 since ordered by length already
		if curr_val > curr_max:
			break

	return 'Highest scoring word pair: {w1} {w2} - score={score}'.format(w1=w1, w2=w2,
																			 score=_get_pair_score(w1, w2))

	#	# if here and then all prev comparisons resulted in 0 so just return the last pair
	#	return 'Highest scoring word pair: {w1} {w2} - score=0'.format(w1=w1, w2=w2)


"""
	Returns:
		List comprising contents of file
"""
def read_file_to_list(word_file='words_shuf_110k.txt'):
	file = open(word_file, 'r')
	word_list = []
	words = file.readlines()
	for idx in range(len(words)):
		word_list.append(words[idx].strip('\n').strip('\r'))
	file.close()
	return word_list


"""
	Returns:
		(new) List sorted by word length (descending)
"""
def sort_list_by_length(list):
	return sorted(list, key=len, reverse=True)


"""
	Returns:
	 	True if words share common character
		False if words share NO common character
"""
def _shares_common_chars(w1, w2):
	for i in w1:
		if w2.find(i) >= 0:  # non-matches usually return -1 and/or 0
			return True
	return False


"""
	Returns:
	 	product using lengths of words
"""
def _get_pair_score(w1, w2):
	return len(w1) * len(w2)


"""
	Returns:
	 	False if 2 diff words
 		True if words are same value
 		(NOTE: use == when comparing values and is when comparing obj. identity)
"""
def _is_duplicate(w1, w2):
	return w1 == w2
