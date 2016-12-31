import cgi
from .find import Find
from BaseHTTPServer import BaseHTTPRequestHandler

class httpHandler(BaseHTTPRequestHandler):
    
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
            F = Find()
            result = F.find_words(form["word"].value, form["count"].value)
            self.wfile.write(result)
            return