from __future__ import print_function
import subprocess
from threading import Timer
import os
import signal
import sys

def killAndPrint(p):
	os.kill(p.pid, signal.SIGINT)
	#p.kill()
	#print("ahah "+p.stdout.read()+" test")
def lambda_handler(event, context):
	proc = subprocess.Popen("python goldeneye.py " + event['args'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#proc = subprocess.Popen("python goldeneye.py http://www.google.com -s 1 -w 1", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#proc = subprocess.Popen(["python", "goldeneye.py", "http://127.0.0.1", "-s", "1", "-w", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	kill_proc = killAndPrint
	timer = Timer(event['duration'], kill_proc, [proc])
	try:
		timer.start()
		stdout,stderr = proc.communicate()
	finally:
		timer.cancel()
	return stdout + stderr


if __name__=='__main__':
    lambda_handler({'args': ' '.join(sys.argv[1:-1])})
