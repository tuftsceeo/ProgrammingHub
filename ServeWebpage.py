# Dan McGinn, Tufts CEEO
# Run with python3

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, socket, os, webbrowser
import paramiko
# from threading import Thread
# import xml.etree.ElementTree as xml



# Set Content for the Forms
pyCode = {'ev3dev':'''import ev3dev.ev3 as ev3''',
          'Beep':'''ev3.Sound.beep()''',
          'Green':'''ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)\nev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)''',
          'Yellow':'''ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)\nev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)''',
          'Red':'''ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)\nev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)''',
          'Fwd':'''motor_left = ev3.LargeMotor('outB')\nmotor_right = ev3.LargeMotor('outC')\nspeed = 25 # Set Speed\nmotor_left.run_direct(duty_cycle_sp=speed)\nmotor_right.run_direct(duty_cycle_sp=speed)''',
          'Stop':'''speed = 0 # Set Speed to Zero\nmotor_left.run_direct(duty_cycle_sp=speed)\nmotor_right.run_direct(duty_cycle_sp=speed)'''}

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
reply=''
ConnectionFailed=False

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
        pageContent = (open(os.getcwd()+'/includes/LandingV2.html').read())+(open(os.getcwd()+'/includes/LandingV2connect.html').read()%(str(ConnectionFailed)))
    elif page == 'simplePage':
        pageContent = (open(os.getcwd()+'/includes/Base.html').read()%(terminal,page,str(connected)))+(open(os.getcwd()+'/includes/styleSheet.html')).read()+(open(os.getcwd()+'/includes/Simple.html').read())#+(open(os.getcwd()+'/includes/note.xml').read())
    elif page == 'page2':
        pageContent = (open(os.getcwd()+'/includes/Base.html').read()%(terminal,page,str(connected)))+(open(os.getcwd()+'/includes/styleSheet.html')).read() 
        for line in pyCode:
            rows=pyCode[line].count('\n')+1
            pageContent = pageContent + Form_html.format(rows,line,pyCode[line])
    return pageContent

def InitSSH(host,username,password):
    global connected, ssh, channel, page, reply, ConnectionFailed
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username='robot', password='maker', timeout = 5)
        channel = ssh.invoke_shell()
        #print("Connected to %s" % host)
        #print(channel)
        connected = True
        ConnectionFailed=False
        page = 'simplePage'
        reply = channel.recv(9999).decode()
    except:
        ConnectionFailed = True
        print("Connection Failed")
        connected = False #Change to failed and add text to the landing page for failure
        reply = ''
    return connected, ssh, channel, page, reply, ConnectionFailed

def CloseSSH():
    global connected, ssh, channel, page
    if channel != None:
        channel.close()
    if ssh != None:
        ssh.close()
    connected = False
    return connected, page

def WriteSSH(string):
    global ssh, channel, reply, connected
    if ssh != None and channel != None:
        try:
            size = channel.send(string.encode('utf-8'))
        except:
            connected = False
    return connected

def ReadSSH():
    global ssh, channel, reply, connected
    if ssh != None and channel != None and channel.recv_ready():
        reply = channel.recv(9999).decode()
        # if 'Debian' in reply: #Take out ASCII ev3dev logo becuase it doesn't look right in the textbox
        #     reply = "\nDebian"+reply.split("Debian")[1]
    else: 
        connected = False
        reply = ''
        CloseSSH()
    return reply, connected

def printTerminal(reply):
    global terminal
    terminal = terminal+reply
    return terminal

def clearTerminal():
    global terminal
    terminal =''
    return terminal

def refreshTerminal(CurrentReply):
    global ssh, channel, connected
    if ssh != None and channel != None and channel.recv_ready():
        reply = channel.recv(9999).decode()
    # else:
    #     reply=''
    # if reply != CurrentReply:
        printTerminal(reply)

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
        mimetype='text/javascript'
    elif path.endswith(".css"):
        mimetype='text/css'
    elif path.endswith(".ico"):
        mimetype='image/vnd.microsoft.icon'
    else:
        mimetype='text/html'
    return mimetype

def parseDevice(post_data):
    global Device,Username,Password,IP
    Device = ((post_data.split('device='))[1].split('&')[0])
    Username = ((post_data.split('username='))[1].split('&')[0])
    Password = ((post_data.split('password='))[1].split('&')[0])
    IP = ((post_data.split('ipAddress='))[1].split('&')[0])
    return Device,Username,Password,IP

# def thread2(CurrentReply):
#     ReadSSH()
#     if reply != CurrentReply:
#         filename = (os.getcwd()+'/includes/note.xml')
#         root = xml.Element("note")
#         userelement = xml.Element("terminalContent")
#         uid = xml.SubElement(userelement, "uid")
#         uid.text = reply

# Webserver
class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self,pageContent):
        self.send_response(200)
        #print("self.path: %s" % (self.path))
        SetMimeType(self.path)
        #print("mimetype: %s" % (mimetype))
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
        setPageContent(page)
        self.wfile.write(pageContent.encode("utf-8"))

    def do_POST(self):
        global ssh, connected, page
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        print(post_data)
        if 'device' in post_data:
            parseDevice(post_data)
            InitSSH(IP,Username,Password)
            if connected == True:
                sleep(1)
                ReadSSH()
                printTerminal(reply)
            #print("Reply: %s" % reply)
        else:
            post_data = post_data.split("=")[1]  # Only keep the value
            #print(post_data) # Uncomment for debugging
        setPage(post_data) # Change page
        # readCommands(post_data) # Read Commands from Forms
        # if 'Connect' in post_data: # Code for original Landing Page
        #     ip = post_data.split("&")[0]
        #     InitSSH(ip,'robot','maker')
        #     sleep(.75)
        #     ReadSSH()
        #     printTerminal(reply)
        #     print("Reply: %s" % reply)
        if 'Close' in post_data:
            CloseSSH()
        elif 'SendCommand' in post_data:
            command = unquote(post_data.split("&")[-2].replace("+", " "))
            #print("Command: %s" % command)
            WriteSSH(command+'\n')
            if 'python' in post_data: #opening a python session takes more time
                sleep(3)
                if '3' in post_data:
                    sleep(.75)
            else:
                sleep(.5)
            if connected == True:
                ReadSSH()
                printTerminal(reply)
            if connected == False:
                clearTerminal()
            #print("Reply: %s" % reply)
        elif 'Clear' in post_data:
            clearTerminal()
        elif 'Refresh' in post_data:
            print('refreshing...')
            refreshTerminal(reply)
        elif 'REPL' in post_data:
            print(post_data)
            command = unquote(post_data.split("&")[-2].replace("+", " "))
            lines=len(command.splitlines())
            print("Lines: %s" % lines)
            for i in range(0, lines):
                #print("Command: %s" % (command.splitlines()[i]))
                WriteSSH(command.splitlines()[i]+'\n')
                if 'import' in command:
                    sleep(1)
                else:
                    sleep(.1)
                ReadSSH()
                printTerminal(reply)
        self._redirect('/')  # Redirect back to the root url
        return ssh, connected, page

# Create Webserver
if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    #http_server.listen(host_port, address='project_name.io')
    print("Server Starts - %s:%s" % (ip_address, host_port))
    webbrowser.open_new('http://%s:%s' %  (ip_address, host_port)) # Open in browser automatically

    try:
        http_server.serve_forever()
        # Thread(target = http_server.serve_forever()).start()
        # Thread(target = thread2(reply)).start()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
