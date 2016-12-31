import cgi
import sys
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8082
expected_len = int(sys.argv[2])
valid_letters = sys.argv[1]
words = []
words_step_2 = []
valid_letters_array = []
words_with_multi_letter = []

for v in valid_letters:
    valid_letters_array.append(v)

#init value
tx_valid_letters_array = valid_letters_array

def update_given_letters(startindex=None,tx_valid_letters_array=None):
    result  = None
    if startindex is not None:
        del tx_valid_letters_array[startindex]
        result = tx_valid_letters_array
    else:
        result = tx_valid_letters_array
    return result

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
    for words in result:
        print words
    print '--'*50


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("<form method='post' action='/'>")
        self.wfile.write("<input name='word' type='text'>")
        self.wfile.write("<input name='count' type='text'>")
        self.wfile.write("<input type='submit' value='Find'>")
        self.wfile.write("</form>")
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
            print 'form:',form
            print "Your name is: %s" % form["word"].value
            print "Your name is: %s" % form["count"].value
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Thanks %s !" % form["word"].value)
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
    