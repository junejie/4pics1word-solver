import sys


expected_len = int(sys.argv[2])
words = []
words_step_2 = []
valid_letters = sys.argv[1]
valid_letters_array = []
for v in valid_letters:
    valid_letters_array.append(v)

step_4_to_remove = []

#init value
tx_valid_letters_array = valid_letters_array

def temp_update(startindex=None,tx_valid_letters_array=None):
    tmp  = None
    if startindex is not None:
        del tx_valid_letters_array[startindex]
        tmp = tx_valid_letters_array
    else:
        tmp = tx_valid_letters_array
    return tmp

with open('words.txt') as file:
# with open('words.txt') as file:
# with open('words_sample.txt') as file:
    start = 0
    for line in file:
        line_no_enter = line.strip('\n')
        if len( line_no_enter ) == expected_len:
            words.append(line_no_enter)
            start =start+1
    print 'found',len(words), 'words with', expected_len, 'chars'


    # letter count is ok but letter match is wrong
    step_2 = 0
    word_to_remove = []
    for word in words:
        t_valid_letters_array = valid_letters_array
        last = False
        for letter in word:
            foundLetter = letter in t_valid_letters_array
            print '--',foundLetter
            if foundLetter == False:
                word_to_remove.append(word)

    print 'invalid:', word_to_remove


    # check letter dupplication
    # step 3
    print 'step 3....'
    newWordSet = set(words) ^ set(word_to_remove)

    # start letter by letter
    for n in newWordSet:

        valid_letters_array = []
        for v in valid_letters:
            valid_letters_array.append(v)

        tx_valid_letters_array = valid_letters_array
        # print 'valid_letters_array',valid_letters_array
        # print '----------------'*5,'word;',n
        for ltr_in_word in n:
            # print '--find letter',ltr_in_word, 'in', temp_update(None,tx_valid_letters_array)

            # check if no more available letter in array choices
            # means naubusan ng letter
            # use simple if
            basicCheck = ltr_in_word in temp_update(None,tx_valid_letters_array)
            if basicCheck:
                startindex = 0
                for v in temp_update(None,tx_valid_letters_array):
                    if ltr_in_word == v:
                        # print '--found in', startindex, 'index', startindex ,'to be remove'
                        # do remove
                        temp_update(startindex,tx_valid_letters_array)
                        break;
                    startindex = startindex+1
            else:
                step_4_to_remove.append(n)

    print '--'*50
    result = set(newWordSet) ^ set(step_4_to_remove)
    for a in result:
        print a
    print '--'*50
