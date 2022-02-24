import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from analyse import analyse
from get_transcript import Code, Transcript



class Card:
    def __init__(self, txt, name, location):
        self.txt = txt
        self.name = name
        self.location = location

    def toJSON(self):
        return self.__dict__

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/hello'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, this is from http:://xxx/hello!')
        elif self.path.startswith('/meetingid/'):
            self.send_response(303)
            self.send_header('Location', 'https://zoom.us/oauth/authorize?response_type=code&client_id=mBr4CQ7wR8KlxZcISGMsyA&redirect_uri=http://localhost:8000')
            self.end_headers()
            global id
            id = int(self.path[11:])
            self.wfile.write("{a}".format(a=id).encode("utf-8"))
        elif self.path.startswith('/?code='):
            transcript = Transcript(id, client_key="mBr4CQ7wR8KlxZcISGMsyA", client_secret="533Kdl2aa0w2Kvbb9Z5QcIizWLn3VJWQ", code=self.path[7:]).GetTranscript()
            print(id)
            print(transcript)
            if transcript == None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Error - Meeting transcript not found. Either the meeting ID is invalid, or the audio transcript is not done transcribing.')
            else:
                self.send_response(303)
                self.send_header('Location', 'http://127.0.0.1:5500/myfront/newpage.html')
                self.end_headers()
                #self.wfile.write("{a}, {b}".format(a=transcript, b=self.path[7:]).encode("utf-8"))
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
