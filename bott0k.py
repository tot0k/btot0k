'''
	@totok (twitter.com/redtotok)
	project botT0k - ask me before using my code please.
	made with Twitch-API : https://github.com/justintv/Twitch-API/blob/master/IRC.md
'''

import socket
from settings import *
from time import sleep, time, strftime
from commands import *
from threading import Thread
from tkinter import *

class Bot(Thread):
	def __init__(self,can, channel,connectMessage):
		Thread.__init__(self)
		self.channel = channel
		self.updateTime = 30
		self.idle = True
		self.lastUpdate = int(time())
		self.can = can
		
		self.graphics()

		self.s = socket.socket()
		updateLists(self.channel)
		self.connect()

		if self.idle:
			self.joinRoom()
			if connectMessage:
				self.sendMessage("Salut à tous ! MrDestructoid . Je suis botT0k, le bot de t0t0k :) Tapez !help pour plus d'infos :)")


	def connect(self):
		try:
			print("trying to connect to #{}...".format(self.channel))
			self.chat("trying to connect to #{}...".format(self.channel))
			self.s.connect((HOST, PORT))
			self.s.send(("PASS " + PASS + "\r\n").encode('utf-8'))
			self.s.send(("NICK " + NICK + "\r\n").encode('utf-8'))
			self.s.send(("JOIN " + "#"+ self.channel + "\r\n").encode('utf-8'))
		except TimeoutError:
			print("Error : the server didn't answer.")
			self.chat("Error : the server didn't answer.")
	
			self.idle = False

	def joinRoom(self):
		readbuffer = ""
		loading = True

		while loading:
			readbuffer += self.s.recv(1024).decode('utf-8')
			tempList = readbuffer.split("\n")
			readbuffer = tempList.pop()
			for line in tempList:
				if("End of /NAMES list" in line):
					print("*** CONNECTED TO #{} ***".format(self.channel))
					self.chat("*** CONNECTED TO #{} ***".format(self.channel) + '\n')
					loading = False

	def sendMessage(self, message):
		self.s.send(("PRIVMSG " + "#"+self.channel + " :" + message + "\r\n").encode('utf-8)'))
		print("sent > " + message)
		self.chat("sent > " + message)

	def chat(self,message):
		self.chatBox.config(state=NORMAL)
		self.chatBox.insert(END, message + '\n')
		self.chatBox.config(state=DISABLED)
		self.can.update()

	def graphics(self):
		self.chatBox = Text(self.can,height=50,width=112)
		self.chatBox.pack(padx=5,pady=5)

		# Send messages with bot
		self.inputUser = StringVar()
		self.inputField = Entry(self.can, text=self.inputUser,width=150)
		self.inputField.pack(side=TOP,padx=5,pady=5)
		self.inputField.bind("<Return>", self.enterPressed)
		self.can.update()

	def enterPressed(self,event):
		if self.inputUser.get()!="":
			self.sendMessage(self.inputUser.get())
			self.inputUser.set("")


	def run(self):
		while self.idle:
			try:
				readbuffer = self.s.recv(1024).decode('utf-8')

				if readbuffer == "PING :tmi.twitch.tv\r\n":
					s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

				tempList = readbuffer.split("\n")
				readbuffer = tempList.pop()

				for line in tempList:
					tab = line.split(":")
					username = tab[1].split("!")[0]		# Catching username in the 2nd part of the split, before the first '!'

					message = tab[2][:len(tab[2]) - 1]	# Catching message
					print(username + " > " + message)
					self.chat(username + " > " + message)

					if message[0] == "!":				# Detecting commands
						answers = command(username,message)
						print("command")
						while answers != [None]:
							self.sendMessage(answers[0])
							answers.pop(0)
							sleep(0.2)
			except:
				pass
			sleep(0.1)

			if int(time()) - self.lastUpdate > self.updateTime:		# Updating admin, commands and viewers lists
				self.lastUpdate = int(time())
				updateLists(self.channel)


class Application(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title("Bott0k - TwitchBot")	
		self.main = Canvas(self, width=300, height=120, bg="light grey",border=0)
		self.main.pack(side=TOP)

		validateButton = Button(self.main, text = "Connect", command = self.activateBot, width=15, bg="light grey")
		self.main.create_text(150,15,text="Enter channel name",font=("BAUHS93",18,'bold'))
		self.main.create_line(0,35,300,35, width = 2)

		self.channel = StringVar()
		self.check = IntVar()
		self.channel.set("t0t0k")

		menu = OptionMenu(self.main, self.channel, "t0t0k", "lacommu7arg", "kokuho","kayucha","sednegi")
		saisieChannel = Entry(self.main, textvariable = self.channel, width=20)
		checkBox = Checkbutton(self.main, text="MOTD", variable=self.check, bg="light grey")

		saisieChannel.place(x=150,y=45)
		menu.place(x=10,y=40)
		validateButton.place(x=40,y=80)
		checkBox.place(x=180,y=80)

		self.bot = None


	def activateBot(self):
		self.main.destroy()
		self.main = Canvas(self, bg="light grey",border=0)
		self.main.pack(side=TOP)
		self.bot = Bot(self.main, self.channel.get(), self.check.get())
		self.bot.start()

app = Application()
app.mainloop()