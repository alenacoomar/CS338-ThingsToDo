import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from analyse import analyse

class Card:
    def __init__(self, name, time, location):
        self.name = name
        self.time = time
        self.location = location

    def toJSON(self):
        return self.__dict__

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/hello'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, this is from http:://xxx/hello!')
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

        jobs = analyse(str(body))
        testData = []
        for job in jobs:
            testData.append(Card(job, "", "").toJSON())

        response = {"receivedFile": str(body), "todo": testData}
        self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        print("---RECEIVED:", body, "---")

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
