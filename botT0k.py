'''
    @totok (twitter.com/redtotok)
	project botT0k - ask me before using my code please.
	made with Twitch-API : https://github.com/justintv/Twitch-API/blob/master/IRC.md

	main program :
	- connecting to the irc twitch channel
	- waiting for commands

'''



import socket
from settings import *
from time import sleep, time, strftime
from commands import *

run = True
s = socket.socket()
IDLE = 10		# Idle time (in seconds)
lastUpdate = int(time())

def connect(s):
	s.connect((HOST, PORT))
	s.send(("PASS " + PASS + "\r\n").encode('utf-8'))
	s.send(("NICK " + NICK + "\r\n").encode('utf-8'))
	s.send(("JOIN " + CHANNEL + "\r\n").encode('utf-8'))
	return s

# Method for sending a message
def sendMessage(message):
    s.send(("PRIVMSG " + CHANNEL + " :" + message + "\r\n").encode('utf-8)'))
    print("sent > " + message)

def joinRoom(s):
	readbuffer = ""
	loading = True

	while loading:
		readbuffer += s.recv(1024).decode('utf-8')
		tempList = readbuffer.split("\n")
		readbuffer = tempList.pop()
		for line in tempList:
			loading = loadingComplete(line)

def loadingComplete(line):
	if("End of /NAMES list" in line):
		print("*** CONNECTED TO {} ***".format(CHANNEL))
		return False
	else:
		return True

connect(s)
joinRoom(s)

sendMessage("Salut à tous ! MrDestructoid .")

while run :
	readbuffer = s.recv(1024).decode('utf-8')
	tempList = readbuffer.split("\n")
	readbuffer = tempList.pop()

	for line in tempList:
		if (line[0] == "PING"):
			s.send("PONG %s\r\n" % line[1])
			print("pong")
		else:
			tab = line.split(":")
			username = tab[1].split("!")[0]		# Catching username in the 2nd part of the split, before the first '!'

			try :
				message = tab[2][:len(tab[2]) - 1]	# Catching message
				print(username + " > " + message)
			except IndexError:
				message = username

			if message[0] == "!":				# Detecting commands
				answers = command(username,message)
				if answers != [None]:
					for m in answers:
						sendMessage(m)

	if int(time()) - lastUpdate > IDLE:		# Updating admin, commands and viewers lists
		lastUpdate = int(time())
		updateLists()

