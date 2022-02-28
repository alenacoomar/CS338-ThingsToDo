import base64
import http.client
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# url used to get the code that's used to get OAuth access token
# zoom.us/oauth/token?response_type=code&client_id=3inmm7aUQ1uy_zyuKMp3w&redirect_uri=http://localhost:8080
# redirect_uri must be whitelisted when you create the app

# use case: Transcript(meeting_id, access_token=access_token).GetTranscript()
#   or Transcript(meeting_id, client_key=client_key, client_secret=client_secret, code=code).GetTranscript()

class Code():
    def __init__(self, client_key=None):
        self.client_key = client_key
        self.code = None
        self.conn = None
    def GetCode(self):
        """Gets the authorization code"""
        self.conn = http.client.HTTPSConnection("zoom.us")
        self.conn.request("GET", "/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri=http://localhost:8000".format(client_id=self.client_key))
        res = self.conn.getresponse()
        print(res.read())
        response = json.loads(res.read().decode("utf-8"))
        print(response)
        return response

class Transcript():
    """Use the API token's key, secret, and code to get transcript file from cloud recording of meeting with id meeting_id."""
    
    def __init__(self, meeting_id, client_key=None, client_secret=None, code=None, access_token=None):
        """
        Args: 
            client_key (string): Key of api token.
            client_secret (string): Secret of api token.
            code (string): Code created when directed to OAuth URL.
            meeting_id (integer): ID of the meeting you need the transcript for.
        """
        self.meeting_id = meeting_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.code = code
        self.access_token = access_token
        self.conn = None
    
    def GetTranscript(self):
        """Gets the transcript using the parameters the instance has access to."""

        self.conn = http.client.HTTPSConnection("zoom.us")
        #got_file = False
        content = None
        if None in [self.client_key, self.client_secret, self.code] and self.access_token is None:
            print("Zoom OAuth token needed to get transcript.")
            return content

        if self.code is None:
            self.code = self._GetCode()

        if self.access_token is None:
            self.access_token = self._GetAccessToken()

        try:
            download_url = self._GetDownloadUrl()
        except:
            print("Bad Access Token")
            if None in [self.client_key, self.client_secret, self.code]:
                print("client_key, client_secret, and code needed to create access token.")
                return content
            self.access_token = self._GetAccessToken()
            download_url = self._GetDownloadUrl()
        
        if download_url is None:
            print("Meeting Not Found.")
        else:
            transcript = requests.get(download_url, allow_redirects=True)
            #open("{meeting_id}_audio_transcript.vtt".format(meeting_id=self.meeting_id), 'wb').write(transcript.content)
            #got_file = True
            content = transcript.content
        
        return content

    # def _GetCode(self):
    #     #https://zoom.us/oauth/authorize?response_type=code&client_id=mBr4CQ7wR8KlxZcISGMsyA&redirect_uri=http://localhost:8000'
    #     self.conn.request("GET", "/oauth/authorize?response_type=code&client_id=mBr4CQ7wR8KlxZcISGMsyA&redirect_uri=http://localhost:8000")
    #     res = self.conn.getresponse()
    #     response = json.loads(res.read().decode("utf-8"))
    #     print(response)

    def _GetAccessToken(self):
        """Gets an access token using client_key, client_secret, and code."""

        # Encoding client authorization 
        pair = "{client_key}:{client_secret}".format(client_key=self.client_key, client_secret=self.client_secret)
        authorization = base64.b64encode(pair.encode("utf-8")).decode("utf-8")

        # Getting the access token
        access_token_headers = {
            "Authorization": "Basic {authorization}".format(authorization=authorization),
            "Content-Type": "application/x-www-form-urlencoded"
            }
        request_endpoint = "/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=http://localhost:8000".format(code=self.code)
        self.conn.request("POST", request_endpoint, headers=access_token_headers)
        res = self.conn.getresponse()
        response = json.loads(res.read().decode("utf-8"))

        try:
            return response["access_token"]
        except KeyError:
            print("Request for access token failed for the following reason: {reason}".format(reason=response["reason"]))
    
    def _GetDownloadUrl(self):
        """Gets the url needed to download the transcript."""

        # Using access_token to get the transcript for the meeting that's mapped to meeting_id
        get_meeting_headers = {
            'authorization': "Bearer {access_token}".format(access_token=self.access_token),
            'content-type': "application/json"
        }
        try:
            request_endpoint = "/v2/users/me/recordings?from=2000-01-01"
            self.conn.request("GET", request_endpoint, headers=get_meeting_headers)
            res = self.conn.getresponse()
            data = res.read().decode("utf-8")
            response = json.loads(data)
        except:
            print("Bad Response to access recordings.")
        
        # Download the transcript if it exists
        download_url = None
        for meeting in response["meetings"]:
            if "recording_files" not in meeting or meeting["id"] != self.meeting_id:
                continue
            for recording_file in meeting["recording_files"]:
                if "recording_type" not in recording_file:
                    continue
                if recording_file["file_type"] == "TRANSCRIPT": 
                    download_url = "{endpoint}?access_token={access_token}".format(endpoint=str(recording_file["download_url"]), access_token=self.access_token)
        return download_url



if __name__ == '__main__':
    meeting_id = 99707600165 
    access_token = "eyJhbGciOiJIUzUxMiIsInYiOiIyLjAiLCJraWQiOiJkMzRiMTBhMy0xNWY1LTQyYTEtOWRjMi0wNDVkNDI2NTc0YmEifQ.eyJ2ZXIiOjcsImF1aWQiOiI2MTI5OWM3MWYyYTYzMGEyYWI3ZjM1NmJmOWNiYzI5ZSIsImNvZGUiOiJvMWVMYzJoWjU3XzB5UkNZUXg1UVFTVUFoNW9ETHRGa3ciLCJpc3MiOiJ6bTpjaWQ6bUJyNENRN3dSOEtseFpjSVNHTXN5QSIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiIweVJDWVF4NVFRU1VBaDVvREx0Rmt3IiwibmJmIjoxNjQzMTMyNTkxLCJleHAiOjE2NDMxMzYxOTEsImlhdCI6MTY0MzEzMjU5MSwiYWlkIjoiOUttR3dmRXlRMC1wdmJINGlGTl9CQSIsImp0aSI6IjcyZDFjYWE1LWI5MjgtNDM0Ni1hZDZkLTZmNmJhMzQzZTYyZCJ9.YhvvIrmKGg84L5k2m72fvZFuA-1qZfydx4RZxIlDeMQf1kl-3dGJrkiFHpjdvgADwQQYs1wey2UM49YRnCeqgA"
    transcript = Transcript(meeting_id, client_key="mBr4CQ7wR8KlxZcISGMsyA", client_secret="533Kdl2aa0w2Kvbb9Z5QcIizWLn3VJWQ").GetTranscript()
    #transcript = Transcript(meeting_id, client_key="mBr4CQ7wR8KlxZcISGMsyA", client_secret="533Kdl2aa0w2Kvbb9Z5QcIizWLn3VJWQ", access_token="")
    print(transcript)