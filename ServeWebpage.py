# Dan McGinn, Tufts CEEO
# Run with python3

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, socket, os, webbrowser
import paramiko


# Set Content for the Forms
pyCode = {'Beep':'''import ev3dev.ev3 as ev3\nev3.Sound.beep()''',
          'Green':'''import ev3dev.ev3 as ev3\nev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)\nev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)''',
          'Yellow':'''import ev3dev.ev3 as ev3\nev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)\nev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)''',
          'Red':'''import ev3dev.ev3 as ev3\nev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)\nev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)''',
          'Fwd':'''import ev3dev.ev3 as ev3\nmotor_left = ev3.LargeMotor('outB')\nmotor_right = ev3.LargeMotor('outC')\nspeed = 80 # Set Speed\nmotor_left.run_direct(duty_cycle_sp=speed)\nmotor_right.run_direct(duty_cycle_sp=speed)'''}

# HTML for Forms
Form_html = ''' 
<form action="/" method="POST">
   <textarea rows="{}" cols="50" spellcheck="false" name = "{}"
      style = "border:none;resize:none;background-color:powderblue"
   >{}</textarea>
   <input type="submit" name = "REPL" value = ">>>">
</form>
'''

# Initialize global variables
connected = False
page = 'landing'
terminal = ''
pageContent = '''
<html>
<body style="width:960px; margin: 20px auto;">
<h4>There is a problem Loading this page </h4>
</body>
</html>''' # Something very bad has happened if you see this

ssh = None
channel = None

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
    if 'simplePage' in post_data or 'Skip' in post_data:
        page = 'simplePage'
    elif 'page2' in post_data:
        page = 'page2'
    elif 'Return' in post_data:
        page = 'landing'
    return page

def setPageContent(page):
    global pageContent
    if page == 'landing':
        pageContent = (open(os.getcwd()+'/includes/Landing.html').read())
    elif page == 'simplePage':
        pageContent = (open(os.getcwd()+'/includes/Base.html').read()%(terminal,page,str(connected)))+(open(os.getcwd()+'/includes/styleSheet.html')).read()+(open(os.getcwd()+'/includes/Simple.html').read())
    elif page == 'page2':
        pageContent = (open(os.getcwd()+'/includes/Base.html').read()%(terminal,page,str(connected)))+(open(os.getcwd()+'/includes/styleSheet.html')).read() 
        for line in pyCode:
            rows=pyCode[line].count('\n')+1
            pageContent = pageContent + Form_html.format(rows,line,pyCode[line])
    return pageContent

# def readCommands(post_data):
#     if 'REPL' in post_data:
#         LinesOfCode = unquote(post_data.split("&")[0].replace("+", " ")).split('\n')
#         print(LinesOfCode)
#         return LinesOfCode

def InitSSH(host,username,password):
    global connected, ssh, channel, page, reply,ev3dev
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username='robot', password='maker', timeout = 5)
        channel = ssh.invoke_shell()
        #print("Connected to %s" % host)
        #print(channel)
        connected = True
        page = 'simplePage'
        reply = channel.recv(9999).decode()
    except:
        print("Connection Failed")
        connected = False #Change to failed and add text to the landing page for failure
        reply = ''
    return connected, ssh, channel, page, reply

def CloseSSH():
    global connected, ssh, channel, page
    if channel != None:
        channel.close()
    if ssh != None:
        ssh.close()
    page = 'landing'
    connected = False
    return connected, page

def WriteSSH(string):
    global ssh, channel, reply
    if ssh != None and channel != None:
        size = channel.send(string.encode('utf-8'))

def ReadSSH():
    global ssh, channel, reply
    if ssh != None and channel != None and channel.recv_ready():
        reply = channel.recv(9999).decode()
        if 'Debian' in reply: #Take out ASCII ev3dev logo becuase it doesn't look right in the textbox
            reply = "\nDebian"+reply.split("Debian")[1] 
    return reply

def printTerminal(reply):
    global terminal
    terminal = terminal+reply
    return terminal

def clearTerminal():
    global terminal
    terminal =''
    return terminal

def refreshTerminal(CurrentReply):
    ReadSSH()
    if reply != CurrentReply:
        printTerminal(reply)

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
        global ssh, connected, page
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value
        print(post_data) # Uncomment for debugging
        setPage(post_data) # Change page
        # readCommands(post_data) # Read Commands from Forms
        if 'Connect' in post_data:
            ip = post_data.split("&")[0]
            InitSSH(ip,'robot','maker')
            sleep(.75)
            ReadSSH()
            printTerminal(reply)
            print("Reply: %s" % reply)
        elif 'Close' in post_data:
            CloseSSH()
        elif 'SendCommand' in post_data:
            command = unquote(post_data.split("&")[-2].replace("+", " "))
            #print("Command: %s" % command)
            WriteSSH(command+'\n')
            if 'python' in post_data: #opening a python session takes more time
                sleep(2.5)
                if '3' in post_data:
                    sleep(.75)
            else:
                sleep(.5)
            ReadSSH()
            printTerminal(reply)
            #print("Reply: %s" % reply)
        elif 'Clear' in post_data:
            clearTerminal()
        elif 'Refresh' in post_data:
            refreshTerminal(reply)
        elif 'REPL' in post_data:
            command = unquote(post_data.split("&")[-2].replace("+", " "))
            WriteSSH(command+'\n')
            sleep(.5)
            ReadSSH()
            printTerminal(reply)
        self._redirect('/')  # Redirect back to the root url
        return ssh, connected, page

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
