from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, socket, os, webbrowser

print((open(os.getcwd()+'/includes/BlinkRed.css')).read())