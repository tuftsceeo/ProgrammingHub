# Dan McGinn, Tufts CEEO
# Run with python3

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, telnetlib, socket, os, webbrowser, ssl

# Initialize global variables
page = 'landing'
terminal = ''
pageContent = '''
<html>
<body style="width:960px; margin: 20px auto;">
<h4>There is a problem Loading this page </h4>
</body>
</html>'''

# Get IP Address
ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
s.close()

# Set host port
host_port = 8000

def setPage(post_data):
    global page
    if 'simplePage' in post_data:
        page = 'simplePage'
    elif 'page2' in post_data:
        page = 'page2'
    return page

def setPageContent(page):
    global pageContent
    if page == 'landing':
        pageContent = (open('Landing.html').read())
    elif page == 'simplePage':
        pageContent = (open('Base.html').read()%(terminal,page))+(open('Simple.html').read())
    elif page == 'page2':
        pageContent = (open('Base.html').read()%(terminal,page))+(open('Page2.html').read())
    return pageContent

# Webserver
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
        #print('page = ' + page)
        self.do_HEAD()
        setPageContent(page)
        self.wfile.write(pageContent.encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value
        print(post_data) # Uncomment for debugging
        setPage(post_data) # Change page
        self._redirect('/')  # Redirect back to the root url

# Create Webserver
if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))
    webbrowser.open_new('http://%s:%s' %  (ip_address, host_port)) # Open in browser automatically

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
