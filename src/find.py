import sys

class Find():


    def update_given_letters(self, startindex=None,tx_valid_letters_array=None):
    
        result  = None
        if startindex is not None:
            del tx_valid_letters_array[startindex]
            result = tx_valid_letters_array
        else:
            result = tx_valid_letters_array
        return result

    def find_words(self, valid_letters, expected_len):
        print 'processing...', valid_letters
        print 'processing...', expected_len
        expected_len = int(expected_len)
        words = []
        words_step_2 = []
        valid_letters_array = []
        words_with_multi_letter = []
        for v in valid_letters:
            valid_letters_array.append(v)
        #init value
        tx_valid_letters_array = valid_letters_array

        with open('words.txt') as file:
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
                for letter in word:
                    foundLetter = letter in t_valid_letters_array
                    if foundLetter == False:
                        word_to_remove.append(word)

            # check letter dupplication
            newWordSet = set(words) ^ set(word_to_remove)

            # start letter by letter
            for word in newWordSet:
                valid_letters_array = []
                for valid_letter in valid_letters:
                    valid_letters_array.append(valid_letter)

                tx_valid_letters_array = valid_letters_array
                for ltr_in_word in word:
                    # check if no more available letter in array choices
                    # means naubusan ng letter
                    # use simple if
                    ltr_not_available = ltr_in_word in self.update_given_letters(None,tx_valid_letters_array)
                    if ltr_not_available:
                        startindex = 0
                        for given_letter in self.update_given_letters(None,tx_valid_letters_array):
                            if ltr_in_word == given_letter:
                                # do remove
                                self.update_given_letters(startindex,tx_valid_letters_array)
                                break;
                            startindex = startindex+1
                    else:
                        words_with_multi_letter.append(word)

            print '--'*50
            result = set(newWordSet) ^ set(words_with_multi_letter)
            print result
            return result

