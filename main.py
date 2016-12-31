import cgi
import sys
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8082
# expected_len = int(sys.argv[2])
# valid_letters = sys.argv[1]


def update_given_letters(startindex=None,tx_valid_letters_array=None):
    result  = None
    if startindex is not None:
        del tx_valid_letters_array[startindex]
        result = tx_valid_letters_array
    else:
        result = tx_valid_letters_array
    return result


def find_words(valid_letters, expected_len):
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
                ltr_not_available = ltr_in_word in update_given_letters(None,tx_valid_letters_array)
                if ltr_not_available:
                    startindex = 0
                    for given_letter in update_given_letters(None,tx_valid_letters_array):
                        if ltr_in_word == given_letter:
                            # do remove
                            update_given_letters(startindex,tx_valid_letters_array)
                            break;
                        startindex = startindex+1
                else:
                    words_with_multi_letter.append(word)

        print '--'*50
        result = set(newWordSet) ^ set(words_with_multi_letter)
        print result
        return result

# print find_words(valid_letters, expected_len)

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        html = """
        <style>
            div {
                margin: 10px;
            }
            span.ltr {
                margin-left: 30px;
            }
            .submit {
                margin-left: 100px;
                margin-top: 20px;
            }
        </style>
        <form method='post' action='/'>
            <div>
                <span class='ltr'>Letter: </span>
                <input name='word' type='text'>
            </div>
            <div>
                <span class='slot'>Slot Count:</span>
                <input name='count' type='text'>
            </div>
            <div class='submit'>
                <input type='submit' value='Find'>
            </div>
        </form>
        """
        self.wfile.write(html)
        return

    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/":

            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            self.send_response(200)
            self.end_headers()
            result = find_words(form["word"].value, form["count"].value)
            self.wfile.write(result)
            return      

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
    