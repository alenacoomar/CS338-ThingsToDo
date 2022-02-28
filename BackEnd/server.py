import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from analyse import analyse
from get_transcript import Transcript



class Card:
    def __init__(self, txt, name, location):
        self.txt = txt
        self.name = name
        self.location = location

    def toJSON(self):
        return self.__dict__

authcode = None

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authcode
        if self.path.endswith('/hello'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, this is from http:://xxx/hello!')
        elif self.path.startswith('/?code='):
            self.headers.add_header("authcode", self.path[7:])
            authcode = self.path[7:]
            print(authcode)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("{a}".format(a=self.path[7:]).encode("utf-8"))
            
        elif self.path.startswith('/transcript/'):
            client_id = int(self.path[12:])
            code = authcode
            while code == None:
                code = authcode
            
            transcript = Transcript(client_id, client_key="mBr4CQ7wR8KlxZcISGMsyA",client_secret="533Kdl2aa0w2Kvbb9Z5QcIizWLn3VJWQ", code=code).GetTranscript()
            if transcript == None:
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b'Error - Meeting transcript not found. Either the meeting ID is invalid, or the audio transcript is not done transcribing.')
            else:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                jobs, assignees = analyse(transcript.decode("utf-8"))
                print(jobs, assignees)
                testData = []
                for i in range(len(jobs)):
                    testData.append(Card(jobs[i], assignees[i], "").toJSON())
                response = { "todo": testData}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        jobs, assignees = analyse(str(body.decode("utf-8")))
        print(jobs, assignees)
        testData = []
        for i in range(len(jobs)):
            testData.append(Card(jobs[i], assignees[i], "").toJSON())

        response = { "todo": testData}
        self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        # print("---RECEIVED:", body, "---")


httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
