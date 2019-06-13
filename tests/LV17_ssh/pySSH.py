# Chris Rogers

from time import sleep
from http.server import BaseHTTPRequestHandler,HTTPServer
import json, paramiko

# Set host port
host_port = 8000
ip_address = 'localhost'

gSSHRef = None
gchannel = None

def initSSH(server,username,password):
    global gSSHRef, gchannel

    reply = 'already there'
    if gSSHRef == None:
        gSSHRef = paramiko.SSHClient()
        gSSHRef.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(server + username + password)
        try:
            result = gSSHRef.connect(server, username=username, password=password, timeout = 5)
            gchannel = gSSHRef.invoke_shell()
            gchannel.settimeout(0)
        except:
            result = 'could not connect\r\n'
        reply = str(result)

    return reply

def closeSSH():
    global gSSHRef, gchannel
    if gchannel != None:
        gchannel.close()
    if gSSHRef != None:
        gSSHRef.close()
    gSSHRef = None
    gchannel = None
    return True

def writeSSH(string):
    reply = 'write:no reference\r\n'
    if gSSHRef != None:
        reply = 'write:no connection\r\n'
        if gchannel != None:
            size = gchannel.send(string.encode())
            reply = str(size)
    return reply

def readSSH():
    reply = 'read:no reference\r\n'
    if gSSHRef != None:
        reply = 'read:no connection\r\n'
        if gchannel != None:
            reply = ''
            if gchannel.recv_ready():
                reply = gchannel.recv(9999).decode()

    return(reply)

class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):

        self.do_HEAD()

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        data = json.loads(post_data)
        if not 'read' in data:
            print(data)
        if 'test' in data:
            print(data['test'])
            pageContent = 'got: ' + data['test']
        elif 'init' in data:
            server = data['init']
            pageContent = 'init: ' + str(initSSH(server,"robot","maker"))
        elif 'write' in data:
            pageContent = 'wrote: ' + writeSSH(data['write'])
        elif 'wait' in data:
            reply = ''
            while not data['wait'] in reply:
                sleep(1)
                reply = reply + readSSH()
                #print(reply)
            pageContent = 'wait: ' + reply
        elif 'read' in data:
            read_data = readSSH()
            if read_data.__len__() > 0:
                print(read_data)
            pageContent = 'read: ' + read_data
        elif 'close' in data:
            success = closeSSH()
            pageContent = 'closed' if success else 'failed to close'
        else:
            pageCommand = 'Not Supported Command'

        self.wfile.write(pageContent.encode("utf-8"))
       

# Create Webserver
if __name__ == '__main__':

    http_server = HTTPServer((ip_address, host_port),MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")


'''
class MySSH():
    def __init(server,username,password):
        self.server = server
        self.username = username
        self.password = password
        self.gSSHRef = None
        gchannel = None
    def init():
        reply = 'already there'
        if self.gSSHRef == None:
            self.gSSHRef = paramiko.SSHClient()
            self.gSSHRef.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            result = self.gSSHRef.connect(self.server, self.username, self.password, timeout = 5)
            reply = str(result)
            gchannel = self.gSSHRef.invoke_shell()
            gchannel.settimeout(0)
        return reply
    def close():
        if gchannel != None:
            gchannel.close()
        if gSSHRef != None:
            gSSHRef.close()
        return True
    def write(string):
        reply = 'no reference'
        if gSSHRef != None:
            reply = 'no file'
        if gchannel != None:
            size = gchannel.send(string.encode())
            reply = str(size)
        return reply
    def read()
        reply = 'no reference'
        if gSSHRef != None:
            reply = 'no file'
            if gchannel != None:
                reply = ''
                if gchannel.recv_ready():
                    reply = gchannel.recv(9999).decode()

        return(reply)
        '''
