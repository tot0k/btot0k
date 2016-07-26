'''
    @totok (twitter.com/redtotok)
	project botT0k - ask me before using my code please
	made with Twitch-API : https://github.com/justintv/Twitch-API/blob/master/IRC.md

	commands :
	- updating lists
	- validating commands
	- formating commands
	- sending commands
	- returning bot messages

'''

from time import time, strftime, sleep
from settings import *
from listsHandler import *

COMMAND_LIST = getList('commands')
ADMIN_LIST = getList('admins')
VIEWER_LIST = getList('viewers')
BOT_NAME = "botT0k"
answers = []

# Updating lists
def updateLists():
	global COMMAND_LIST, ADMIN_LIST, VIEWER_LIST
	COMMAND_LIST = getList('commands')
	ADMIN_LIST = getList('admins')
	VIEWER_LIST = getList('viewers')
	#DEBUG print("{}\n{}\n{}".format(COMMAND_LIST,ADMIN_LIST,VIEWER_LIST))

# Saving command and argument, and launching command
def command(user, message):
	# Adding \ to dashes
	tempMessage = ""
	for l in message:
		if l == "\'" or l == "\"":
			tempMessage += "\\"
		tempMessage += l
	message = tempMessage

	answers = []

	tempList = message.split(" ",1)

	command = tempList[0][1:]	# Catching command without '!'

	if len(tempList) == 2:
		sendCommand = command + '("{}","{}")'.format(user,tempList[1])	# Command with argument
	else:
		sendCommand = command + '("{}","")'.format(user)					# Command without argument

	if command in COMMAND_LIST:
		try :
			answers += eval(sendCommand)
		except NameError:
			print("La commande n'est pas implémentée : " + sendCommand)
	else:
		answers += ["Unknown command : " + command]
	return answers

# Checking if the user is an admin
def right(user):
	if user in ADMIN_LIST :
		return True
	else:
		return False

def noRight(user):
	return "/w "+ user + " Vous n'avez pas le droit d'utiliser cette commande."

def isViewer(viewer):
	if viewer in VIEWER_LIST:
		return True
	else:
		return False

def notViewer(user, arg):
	return ["/w {} {} n'est pas un viewer (ou n'est pas encore détecté, attends un peu et réessayes ;) ).".format(user,arg)]

# ------------- ADMINISTRATION --------------

# Debug command
def ping(user,arg):
	if right(user):
		msg = ["pong !"]
		msg += ["il est actuellement " + strftime("%H:%M:%S")]
	else:
		msg = [noRight(user)]

	return msg

# TODO : SECT MODE FOR ANNOUNCES
def annonce(user,arg):
	if right(user):
		msg = ["Bienvenue sur le live de t0t0k !"]
		msg += ["Tapez !help pour avoir la liste des commandes accessibles ;)."]
		return msg
	else:
		return [noRight(user)]

# Clear chat
def clear(user, arg):
	if right(user):
		return ["/clear"]
	else:
		return [noRight(user)]

# Timeout 1 sec
def to(user, arg):
	if right(user):
		if isViewer(arg.lower()):
			return ["/timeout {} 1".format(arg)]
		else:
			return ["/w {} le viewer {} n'existe pas.".format(user, arg)]
	else:
		return [noRight(user)]

# ------------- OTHERS ----------------------

def help(user, arg):
	msg = ["/w {} Salut ! Je suis {}, un bot créé pour ajouter un peu de fun et d'interractions dans le chat de ce live :).".format(user,BOT_NAME)]
	msg += ["/w {} Pour accéder à la liste des commandes disponibles, c'est ici : https://goo.gl/t851kq".format(user)]
	msg += ["/w {} Bon visionage !".format(user)]

	return msg

def salut(user,arg):
	return ["Salut {}, quoi de neuf depuis la dernière fois ?".format(user)]

def beer(user,arg):
	if arg.lower() == BOT_NAME.lower():
		return ["Non merci, je ne bois pas... Par contre je ne suis pas contre un peu d'huile ;)."]
	elif arg.lower() == "all" and right(user):
		return ["{} offre une bierre à tout le monde ! C'est sa tournée !".format(user)]
	elif arg.lower() == user:
		return ["{} se paye une bière. Alcolo va !".format(user)]
	elif isViewer(arg.lower()):
		return ["{} offre une bierre à {} !".format(user,arg)]
	else:
		return notViewer(user,arg)

def ananas(user,arg):
	if arg.lower() == BOT_NAME.lower():
		return ["Non merci, je ne bois pas... Par contre je ne suis pas contre un peu d'huile ;)."]
	elif arg.lower() == "all" and right(user):
		return ["{} offre un jus d'ananas à tout le monde ! C'est sa tournée !".format(user)]
	elif arg.lower() == user:
		return ["{} se paye un jus d'ananas. C'est bon pour la santé !".format(user)]
	elif isViewer(arg.lower()):
		return ["{} offre un jus d'ananas à {} !".format(user,arg)]
	else:
		return notViewer(user,arg)

def oil(user, arg):
	if arg.lower() == BOT_NAME.lower():
		return ["Normalement je bois pas pendant le service, mais bon, si c'est toi {}, je vais faire un effort :p.".format(user)]
	elif isViewer(arg.lower()):
		msg = ["Tu veux faire boire de l'huile à {}, {} ? Mais tu veux sa mort ou quoi ?".format(arg,user)]
		msg += ["/timeout {} 1".format(user)]
		return msg
	else:
		return notViewer(user,arg)

def hug(user, arg):
	if user.lower() == arg.lower():
		return ["{} se sent très seul(e) et aimerait des calins...".format(user)]
	elif arg.lower() == BOT_NAME.lower():
		return ["Oh oui viens par là {}... attends, t'es majeur(e) au moins ?!".format(user)]
	elif isViewer(arg.lower()):
		return ["{} fait un gros calin à {} <3 .".format(user, arg)]
	else:
		return notViewer(user,arg)
