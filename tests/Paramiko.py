import sys,time,select,paramiko
host = '130.64.95.110'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	ssh.connect(host, username='robot', password='maker', timeout = 5)
	shell = ssh.invoke_shell()
	print("Connected to %s" % host)
	print(shell)
	connected = True
	stdin, stdout, stderr = ssh.exec_command("uptime")
	print(stdout.readlines())
	stdin, stdout, stderr = ssh.exec_command("python3 test.py")
	print(stdout.readlines())
except:
	print("Connection Failed")
	connected = False

print(connected)

# Documentation http://docs.paramiko.org/en/2.5/api/client.html