from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, socket, os, webbrowser
import paramiko

Testpath = '/tests/ImageTest.html'
pageContent = (open(os.getcwd()+Testpath).read())

# Get IP Address
ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
s.close()

def Handler():
    Handler.extensions_map={
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg': 'image/svg+xml',
        '.css': 'text/css',
        '.js':  'application/x-javascript',
        '': 'application/octet-stream', # Default
        }

# Set host port
host_port = 8000

def SetMimeType(path):
    #print("Path: %s" % path)
    global mimetype
    if path.endswith(".jpg"):
        mimetype='image/jpg'
    elif path.endswith(".png"):
        mimetype='image/png'
    elif path.endswith(".gif"):
        mimetype='image/gif'
    elif path.endswith(".js"):
        mimetype='application/javascript'
    elif path.endswith(".css"):
        mimetype='text/css'
    elif path.endswith(".ico"):
        mimetype='image/vnd.microsoft.icon'
    else:
        mimetype='text/html'
    return mimetype

# Webserver
class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self,pageContent):
        self.send_response(200)
        # print("self.path: %s" % (self.path))
        SetMimeType(self.path)
        print("mimetype: %s" % (mimetype))
        self.send_header('Content-type', mimetype)
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        SetMimeType(self.path)
        self.send_header('Content-type', mimetype)
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        #print('page = ' + page)
        self.do_HEAD(pageContent)
        self.wfile.write(pageContent.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value
        self._redirect('/')  # Redirect back to the root url

if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))
    webbrowser.open_new('http://%s:%s' %  (ip_address, host_port)) # Open in browser automatically

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")