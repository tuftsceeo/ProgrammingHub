import paramiko

gSSHRef = None
gchannel = None

def InitSSH(server,username,password):
    global gSSHRef, gchannel

    reply = 'already there'
    if gSSHRef == None:
        gSSHRef = paramiko.SSHClient()
        gSSHRef.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        result = gSSHRef.connect(server, username=username, password=password, timeout = 5)
        reply = str(result)
        gchannel = gSSHRef.invoke_shell()
        gchannel.settimeout(0)
    return reply

def CloseSSH():
    if gchannel != None:
        gchannel.close()
    if gSSHRef != None:
        gSSHRef.close()
    return('done')

def WriteSSH(string):
    reply = 'no reference'
    if gSSHRef != None:
        reply = 'no file'
        if gchannel != None:
            size = gchannel.send(string.encode())
            reply = str(size)
    return reply

def ReadSSH():
    reply = 'no reference'
    if gSSHRef != None:
        reply = 'no file'
        if gchannel != None:
            reply = ''
            if gchannel.recv_ready():
                reply = gchannel.recv(9999).decode()

    return(reply)
