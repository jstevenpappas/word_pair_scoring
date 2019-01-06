"""Word Pair Problem

The Basics
Given a list of words, find a pair with the highest score.
The score is determined by multiplying the lengths of the words by one another.
For instance:
[Spoke, Branch] = 30
   5   *   6    = 30
With the exception that if the words share any letters in common then the pair's score is zero.
For instance, the following pair yields a score of 0 because both words contain the letter 'r' :
[Shrink, Branch] = 0

Some Details

Your method should return a single pair of words.
In the event that multiple pairs tie for the highest score...
    Any of these pairs is an acceptable answer
    Pick one and only one, don't return a list of pairs
Zero, while the lowest possible score, is a valid score
Your method signatures and return values should match our template

"""
import sys

def read_file_to_list(word_file='words_shuf_110k.txt'):
    file = open(word_file, 'r')
    word_list = []
    words = file.readlines()
    for w in words:
        word_to_add = w.strip('\n').strip('\r')
        word_list.append(word_to_add)
    file.close()
    return word_list


def sort_list_by_length(list):
    return sorted(list, key=len, reverse=True)


def get_word_bit_tracker(word):
    word_char_tracker = 0
    for char in word:
        ord_val = ord(char)
        # Sets the n-th bit using ord() val of char
        word_char_tracker |= (1 << ord_val)
    return word_char_tracker


def share_common_chars(word1, word2):
    word1_char_tracker = get_word_bit_tracker(word1)
    word2_char_tracker = get_word_bit_tracker(word2)
    '''if words share common chars, &'ing their bit vectors will yield > 1'''
    return word1_char_tracker & word2_char_tracker > 0



def get_score_word_pair(word1, word2):
    if share_common_chars(word1, word2):
        '''if words share common chars, return 0'''
        return 0
    else:
        '''otherwise, return product of their lengths'''
        return len(word1) * len(word2)



"""
    This never compares a pair more than once

    The strategy used here is:
        1) sort word list in descending order
        2) get the word with the max length
        3) create 2 sublists:
            a) words >= max_len
            b) words == max_len
        4) do a for/for dual loop with >= outside and == 
        on the inside for loop
        5) calculate the score:
            if > 0, store the word-pair and some data
            in a list of candidates
            Since we are comparing from the longest words down,
            our candidates will have the highest likelyhood of 
            being one of the pairs w/ the max score
        6) continue 4&5 until either the list of candidate pairs
        reaches our limit constant or the initial sorted list is
        exhausted
        7) choose the candidate tuple with the max() score
        8) done
        
We could do the full O( n^2 ) possible comparisions
but using a heuristic, we do better since our chances of success are at the beginning
stages of collecting candidate word pairs

# after 5 candidates collected and compared for max()
2,971,111

# max possible iterations using this strategy without using a max_candidates limit
6,686,996,172


closer to O(n*(n-1/2)) (i.e., 6,049,945,000) but asymptotically equiv. to O(n^2)


# just to note, the O(n*n) brute force is the following: 12,100,000,000


"""

def main():

    # optionally provide file via cmdline... tho a default is provided
    if len(sys.argv) > 0:
        word_file = sys.argv[1]

    # read the file provided or the default into a list
    unsorted_list = read_file_to_list(word_file=word_file)

    # sort the file in descending order
    sorted_word_list = sort_list_by_length(unsorted_list)

    # get the max len of the longest word - we use this to curate our word lists
    curr_max_word_len = len(sorted_word_list[0])

    # provide a list to store tuples representing high scoring
    # word pair candidates and some metadata
    candidate_list = list()

    # define a constant to declare max number high scoring word pairs from which
    # we will pick the maximum score... this is a heuristic so we don't iterate over
    # and over forever - remember this alg doesn't find the 'highest score' right away
    # necessarily
    MAX_CANDIDATES = 5

    # track the number of comparisons made and store w/ each word pair so we know
    # after how many comparisons the current high scoring candidate was found
    number_of_comparisons = 0

    # loop while the curr_max len is > 0... this serves as both a guide as to how to
    # build our comparison word lists and also a sentinel/flag to signify when to stop
    # comparing
    while curr_max_word_len > 0:

        # subset of sorted list w/ words >= curr max word length
        words_gte_curr_max = [w for w in sorted_word_list if len(w) >= curr_max_word_len]
        # subset of sorted list w/ words == to curr max word length
        words_eq_curr_max = [w for w in sorted_word_list if len(w) == curr_max_word_len]


        # don't bother comparing lists of words where 1 or another list has 0 candidates...
        words_gte_curr_max_len = len(words_gte_curr_max)
        words_eq_curr_max_len = len(words_eq_curr_max)

        # ... so only test those w/ at least 1 candidate word in each list
        if (words_gte_curr_max_len >= 1) and (words_eq_curr_max_len >= 1):

            #print('\t Length of respective lists: words_gte_curr_max={}  subset_equat_to_words={}'.format(
            #   words_gte_curr_max_len,
            #   words_eq_curr_max_len))

            # iterate over words gte curr_max_len
            for word in words_gte_curr_max:

                # iterate over other words equal to curr_max_len
                for other_word in words_eq_curr_max:

                    # calc the score
                    score = get_score_word_pair(word, other_word)

                    # increment the num comparisons
                    number_of_comparisons += 1

                    # if score non-zero, add to our candidate list
                    if score > 0:
                        candidate_list.append((word, other_word, curr_max_word_len, number_of_comparisons, score))

                        print('\tPotential candidate found with score = {scr}: {w1} {w2}'.format(
                            scr=score,
                            w1=word,
                            w2=other_word))

                # monitor number of viable high scoring word pair candidates accumulated so we can keep
                # program runtime as short as possible while attaining reasonably high score
                if len(candidate_list) >= MAX_CANDIDATES:
                    curr_max_word_len = 0
                    break

        # we did our comparisons for this particular curr_max_word_len so decrement the counter and continue
        curr_max_word_len -= 1

    # iteration is done at this point so that means we have anywhere
    # between 0 and MAX_CANDIDATE number of candidate word pairs...

    # choose the tuple from the candidate list that has the max score
    w1, w2, curr_max, num_comps, score = max(candidate_list, key=lambda item: item[4])


    print('After {num_comps} comparisons, highest scoring word pair out of {max_cands} candidates is the following: {w1} {w2} with score {scr}\n'.format(
        num_comps=num_comps,
        max_cands=MAX_CANDIDATES,
        w1=w1,
        w2=w2,
        scr=score))

    print('Total Number of comparisons made to find {max_cands} high score candidates: {num_comps}\n'.format(
        max_cands=len(candidate_list),
        num_comps=number_of_comparisons))

    # print all the candidate tuples so we can see runner ups
    # format:  (word1, word2, current_max_word_len, total comparisons till now, word pair score)
    for cand_tup in candidate_list:
        print(cand_tup)

if __name__ == "__main__":
    main()
