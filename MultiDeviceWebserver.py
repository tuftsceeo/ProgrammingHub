# Dan McGinn, Tufts CEEO
# Run with python3

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, socket, os, webbrowser
import paramiko
# from threading import Thread
# import xml.etree.ElementTree as xml

#initialize variables used to define page content
DeviceLimit = 25
ipList = [None]*DeviceLimit
ipIndex = 0
IP = [None]*DeviceLimit
speed = [0]*DeviceLimit # For AR Demo

connected = [False]*DeviceLimit
page = ['landing']*DeviceLimit
terminal = ['']*DeviceLimit
pageContent = ['''
<html>
<body style="width:960px; margin: 20px auto;">
<h4>There is a problem Loading this page </h4>
</body>
</html>''']*DeviceLimit

ssh = [None]*DeviceLimit
channel = [None]*DeviceLimit
reply = ['']*DeviceLimit
ConnectionFailed = [False]*DeviceLimit

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
   <textarea class="mono" rows="{}" cols="50" spellcheck="false" name = "{}"
      style = "border:none;resize:none;background-color:powderblue"
   >{}</textarea>
   <input type="submit" name = "REPL" value = ">>>">
</form>
'''

# Get IP Address
ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
s.close()

## Thingworx Section for AR Demo Page
# Thingworx info
with open('appkey.txt', 'r') as file:
    appkey = file.read()
url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/CEEO_Summer_2019/Properties/"
headers = {
        'appKey': appkey,
        'Accept': "application/json",
        'Content-Type': "application/json"
        }
propName ="cone"

# Post property value to thingworx
def thingworxPOST(propName,value):
    propValue = {propName: value}
    requests.request("PUT",url+'*',headers=headers,json=propValue)

# Get property value to thingworx and validate value was posted
def thingworxGET(propName,value):
    propValue = {propName: value}
    getResponse=requests.request("GET",url+propName,headers=headers)
    parsed_json = json.loads(getResponse.text)
    dist = (parsed_json['rows'][0][propName])
    if float(value) == dist:
        print("Property Value Updated")
    else:
        print('Property Value Not Updated')

# Set host port
host_port = 8000

def setPage(post_data):
    global page
    print("ipIndex: %s" % ipIndex)
    if 'simplePage' in post_data or 'Skip' in post_data:
        page[ipIndex] = 'simplePage'
    elif 'page2' in post_data:
        page[ipIndex] = 'page2'
    elif 'lesson' in post_data:
        page[ipIndex] = 'lesson'
    elif 'Return' in post_data:
        page[ipIndex] = 'landing'
    elif 'ARdemo' in post_data:
        page[ipIndex] = 'ARdemo'
    return page

def setPageContent(pagelocal):
    global pageContent,speed
    if pagelocal == 'landing':
        pageContent[ipIndex] = (open(os.getcwd()+'/includes/LandingV2.html').read())+(open(os.getcwd()+'/includes/LandingV2connect.html').read()%(str(ConnectionFailed[ipIndex])))
    elif pagelocal == 'simplePage':
        pageContent[ipIndex] = (open(os.getcwd()+'/includes/Base.html').read()%(terminal[ipIndex],page[ipIndex],str(connected[ipIndex])))+(open(os.getcwd()+'/includes/styleSheet.html')).read()+(open(os.getcwd()+'/includes/Simple.html').read())#+(open(os.getcwd()+'/includes/note.xml').read())
    elif pagelocal == 'page2':
        pageContent[ipIndex] = (open(os.getcwd()+'/includes/Base.html').read()%(terminal[ipIndex],page[ipIndex],str(connected[ipIndex])))+(open(os.getcwd()+'/includes/styleSheet.html')).read() 
        for line in pyCode:
            rows=pyCode[line].count('\n')+1
            pageContent[ipIndex] = pageContent[ipIndex] + Form_html.format(rows,line,pyCode[line])
    elif pagelocal == 'lesson':
        pageContent[ipIndex] = (open(os.getcwd()+'/includes/Base.html').read()%(terminal[ipIndex],page[ipIndex],str(connected[ipIndex])))+(open(os.getcwd()+'/includes/styleSheet.html')).read()+(open(os.getcwd()+'/includes/Lesson.html').read())
    elif pagelocal == 'ARdemo':
        pageContent[ipIndex] = (open(os.getcwd()+'/includes/Base.html').read()%(terminal[ipIndex],page[ipIndex],str(connected[ipIndex])))+(open(os.getcwd()+'/includes/styleSheet.html')).read()+(open(os.getcwd()+'/includes/ARDemo.html').read())%(str(speed[ipIndex]),'')+(open(os.getcwd()+'/includes/ARstyleSheet.html').read())
    return pageContent

def InitSSH(host,username,password):
    global connected, ssh, channel, page, reply, ConnectionFailed
    ssh[ipIndex] = paramiko.SSHClient()
    ssh[ipIndex].set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh[ipIndex].connect(host, username='robot', password='maker', timeout = 5)
        channel[ipIndex] = ssh[ipIndex].invoke_shell()
        #print("Connected to %s" % host)
        #print(channel)
        connected[ipIndex] = True
        ConnectionFailed[ipIndex]=False
        page[ipIndex] = 'simplePage'
        reply[ipIndex] = channel[ipIndex].recv(9999).decode()
    except:
        ConnectionFailed[ipIndex] = True
        print("Connection Failed")
        connected[ipIndex] = False #Change to failed and add text to the landing page for failure
        reply[ipIndex] = ''
    return connected, ssh, channel, page, reply, ConnectionFailed

def CloseSSH():
    global connected, ssh, channel, page
    if channel[ipIndex] != None:
        channel[ipIndex].close()
    if ssh[ipIndex] != None:
        ssh[ipIndex].close()
    connected[ipIndex] = False
    return connected, page

def WriteSSH(string):
    global ssh, channel, reply, connected
    if ssh[ipIndex] != None and channel[ipIndex] != None:
        try:
            size = channel[ipIndex].send(string.encode('utf-8'))
        except:
            connected[ipIndex] = False
    return connected

def ReadSSH():
    global ssh, channel, reply, connected
    print(channel[ipIndex].recv_ready())
    if ssh[ipIndex] != None and channel[ipIndex] != None and channel[ipIndex].recv_ready() != True:
        wait(.1)
    if ssh[ipIndex] != None and channel[ipIndex] != None and channel[ipIndex].recv_ready():
        reply[ipIndex] = channel[ipIndex].recv(9999).decode()
        # if 'Debian' in reply: #Take out ASCII ev3dev logo becuase it doesn't look right in the textbox
        #     reply = "\nDebian"+reply.split("Debian")[1]
    else: 
        connected[ipIndex] = False
        reply[ipIndex] = ''
        CloseSSH()
    return reply, connected

def printTerminal(replyLocal):
    global terminal
    terminal[ipIndex] = terminal[ipIndex]+replyLocal
    return terminal

def clearTerminal():
    global terminal
    terminal[ipIndex] =''
    return terminal

def refreshTerminal(CurrentReply):
    global ssh, channel, connected
    if ssh[ipIndex] != None and channel[ipIndex] != None and channel[ipIndex].recv_ready():
        reply[ipIndex] = channel[ipIndex].recv(9999).decode()
    # else:
    #     reply=''
    # if reply != CurrentReply:
        printTerminal(reply[ipIndex])

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
    global Device,Username,Password,IP,ipIndex
    Device = ((post_data.split('device='))[1].split('&')[0])
    Username = ((post_data.split('username='))[1].split('&')[0])
    Password = ((post_data.split('password='))[1].split('&')[0])
    IP[ipIndex] = ((post_data.split('ipAddress='))[1].split('&')[0])
    return Device,Username,Password,IP,ipIndex

def getClientIP(self):
    global ipList, ipIndex, page
    ClientIP = self.address_string() # Get the Client IP Address
    if ClientIP in ipList: # If the Client IP Address is already on the list
        ipIndex = ipList.index(ClientIP) # Set the ipIndex to the index matching the Client IP
    else: # If the Client IP Address isn't already on the list
        ipIndex = ipList.index(None)
        ipList[ipIndex] = ClientIP # add the client IP to the list
        print('New Client IP Address Added')
        page[ipIndex] = 'landing'  # send the client to the landing page
        setPage('landing')
    return ipList, ipIndex, page

def startARDemo():
    global ssh, channel, reply, connected
    string = '''python3
import ev3dev.ev3 as ev3
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')
speed = 20 # Set Speed
direc = 'Stop'

# Motor commands
def forward(speed):
   motor_left.run_direct(duty_cycle_sp=speed)
   motor_right.run_direct(duty_cycle_sp=speed)

def left(speed):
   motor_left.run_direct( duty_cycle_sp=-speed)
   motor_right.run_direct( duty_cycle_sp=speed)

def right(speed):
   motor_left.run_direct( duty_cycle_sp=speed)
   motor_right.run_direct( duty_cycle_sp=-speed)

def back(speed):
   motor_left.run_direct(duty_cycle_sp=-speed)
   motor_right.run_direct(duty_cycle_sp=-speed)

def stop(speed):
   motor_left.run_direct( duty_cycle_sp=0)
   motor_right.run_direct( duty_cycle_sp=-0)

def setSpeed(NewSpeed):
   global speed
   speed = int(NewSpeed)
   return speed

def drive(direc,speed):
    if direc == 'Forward':
        forward(speed)
    elif direc == 'Backward':
        back(speed)
    elif direc == 'Left':
        left(speed)
    elif direc == 'Right':
        right(speed)
    elif direc == 'Stop':
        stop(speed)

# Define settings for Ultrasonic Sensor
us = ev3.UltrasonicSensor() # Connect ultrasonic sensor to any sensor port
us.mode='US-DIST-CM' # Put the US sensor into distance mode.
units = us.units # reports 'cm' even though the sensor measures 'mm'

# Get distance from Ultrasonic Sensor
def getDist():
    return us.value()/10  # convert mm to cm

# LED commands
def green():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

def yellow():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)

def red():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)

'''
    speed[ipIndex] = 20
    if ssh[ipIndex] != None and channel[ipIndex] != None:
        try:
            size = channel[ipIndex].send(string.encode('utf-8'))
        except:
            connected[ipIndex] = False
    return connected

def runARdemo(post_data):
    global ssh, channel, reply, connected, speed
    if ssh[ipIndex] != None and channel[ipIndex] != None:
        speed[ipIndex]='20'
        if 'Fwd' in post_data:
            string="direc = 'Forward'\n"
        elif 'Left' in post_data:
            string="direc = 'Left'\n"
        elif 'Right' in post_data:
            string="direc = 'Right'\n"
        elif 'Bkwd' in post_data:
            string="direc = 'Backward'\n"
        elif 'Stop' in post_data:
            string="direc = 'Stop'\n"
        elif 'Speed' in post_data:
            speed[ipIndex]=post_data.split('=')[1]
            string="setSpeed("+str(speed[ipIndex])+")\n"
        elif 'Green' in post_data:
            string="green()\n"
        elif 'Yellow' in post_data:
            string="yellow()\n"
        elif 'Red' in post_data:
            string="red()\n"
        string=string+"drive(direc,int(speed))\ndistance = getDist()\n"
        size = channel[ipIndex].send(string.encode('utf-8'))
        #Need to get the distance from the EV3
        #thingworxPOST('cone',distance)
        return speed

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
        getClientIP(self)
        self.do_HEAD(pageContent[ipIndex])
        setPageContent(page[ipIndex])
        self.wfile.write(pageContent[ipIndex].encode("utf-8"))

    def do_POST(self):
        global ssh, connected, page, ipIndex
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        print(post_data)
        getClientIP(self)
        if 'StartARDemo' in post_data:
            startARDemo()
            sleep(10)
            ReadSSH()
            printTerminal(reply[ipIndex])
        if 'ARdemo_' in post_data or 'Speed' in post_data:
            runARdemo(post_data)
            sleep(.2)
            ReadSSH()
            printTerminal(reply[ipIndex])
        if 'device' in post_data:
            parseDevice(post_data)
            InitSSH(IP[ipIndex],Username,Password)
            if connected[ipIndex] == True:
                sleep(1)
                ReadSSH()
                printTerminal(reply[ipIndex])
            #print("Reply: %s" % reply)
        else:
            post_data = post_data.split("=")[1]  # Only keep the value
        setPage(post_data) # Change page
        if 'Close' in post_data:
            CloseSSH()
        elif 'SendCommand' in post_data:
            command = unquote(post_data.split("&")[-2].replace("+", " "))
            WriteSSH(command+'\n')
            if 'python' in post_data: #opening a python session takes more time
                sleep(3)
                if '3' in post_data:
                    sleep(.75)
            else:
                sleep(.5)
            if connected[ipIndex] == True:
                ReadSSH()
                printTerminal(reply[ipIndex])
            if connected[ipIndex] == False:
                clearTerminal()
            if command == 'clear':
                clearTerminal()
        elif 'Clear' in post_data:
            clearTerminal()
        elif 'Refresh' in post_data:
            print('refreshing...')
            refreshTerminal(reply)
        elif 'REPL' in post_data:
            command = unquote(post_data.split("&")[-2].replace("+", " "))
            lines=len(command.splitlines())
            for i in range(0, lines):
                #print("Command: %s" % (command.splitlines()[i]))
                WriteSSH(command.splitlines()[i]+'\n')
                if 'import' in command:
                    sleep(1)
                else:
                    sleep(.15)
                ReadSSH()
                printTerminal(reply[ipIndex])
        elif 'Disconnect' in post_data:
            clearTerminal()
            CloseSSH()
            page[ipIndex] = 'landing'
        elif 'Begin+Python+Session' in post_data:
            WriteSSH('python3'+'\n')
            sleep(3.75)
            if connected[ipIndex] == True:
                ReadSSH()
                printTerminal(reply[ipIndex])
            if connected[ipIndex] == False:
                clearTerminal()
        self._redirect('/')  # Redirect back to the root url
        return ssh, connected, page, ipIndex

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
