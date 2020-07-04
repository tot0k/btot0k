'''
    @totok (twitter.com/redtotok)
	project botT0k - ask me before using my code please
	made with Twitch-API : https://github.com/justintv/Twitch-API/blob/master/IRC.md

'''

from time import time, strftime, sleep
from settings import *
from listsHandler import *
from random import randint


BOT_NAME = "botT0k"
answers = []

# Updating lists
def updateLists(channel):
	global COMMAND_LIST, ADMIN_LIST, VIEWER_LIST
	COMMAND_LIST = getList('commands',channel)
	ADMIN_LIST = getList('admins',channel)
	VIEWER_LIST = getList('viewers',channel)

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
	if viewer.lower() in VIEWER_LIST:
		return True
	else:
		return False

def notViewer(user, arg):
	if arg =="":
		return ["/w {} il faut spécifier sur qui utiliser cette commande !".format(user)]
	else:
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
	msg = ["Salut ! Je suis {}, un bot créé pour ajouter un peu de fun et d'interractions dans le chat de ce live :). Pour accéder à la liste des commandes disponibles, c'est ici : https://goo.gl/t851kq".format(BOT_NAME)]
	return msg

def salut(user,arg):
	return ["Salut {}, quoi de neuf depuis la dernière fois ?".format(user)]

def beer(user,arg):
	if arg.lower() == BOT_NAME.lower():
		return ["Non merci, je ne bois pas... Par contre je ne suis pas contre un peu d'huile ;)."]
	elif arg.lower() == "all" and right(user):
		return ["{} offre une bière à tout le monde ! C'est sa tournée !".format(user)]
	elif arg.lower() == user:
		return ["{} se paye une bière. Alcolo va !".format(user)]
	elif isViewer(arg.lower()):
		return ["{} offre une bière à {} !".format(user,arg)]
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

def diabolo(user,arg):
	if arg.lower() == BOT_NAME.lower():
		return ["Non merci, je ne bois pas... Par contre je ne suis pas contre un peu d'huile ;)."]
	elif arg.lower() == "all" and right(user):
		return ["{} offre un diabolo kiwi à tout le monde ! C'est sa tournée !".format(user)]
	elif arg.lower() == user:
		return ["{} se paye un diabolo kiwi. C'est bon pour la santé !".format(user)]
	elif isViewer(arg.lower()):
		return ["{} offre un diabolo kiwi à {} !".format(user,arg)]
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

def hit(user, arg):
	if user.lower() == arg.lower():
		return ["{} se donne un coup sur la tête... un peu con non ?".format(user)]
	elif arg.lower() == BOT_NAME.lower():
		return ["/me tombe dans les pommes..."]
	elif isViewer(arg.lower()):
		return ["{} frappe {} d'un grand coup... méchant !".format(user, arg)]
	else:
		return notViewer(user,arg)

def miss(user, arg):
	return ["Lulu__my on sait que t'es là !"]

def toktok(user, arg):
	if user.lower() == "tot0k":
		return ["Qui est là ?"]
	else:
		msg = ["C'est TO-TOK, pas TOK TOK !"]
		msg += ["MrDestructoid Exterminer, exterminer ! MrDestructoid"]
		return msg

def mouchoir(user, arg):
	if user.lower() == "kayucha":
		return ["Ah, tu vas nous dire ?"]
	else:
		msg = ["On veut savoir kayucha !"]
		return msg

def roll(user, arg):
	msg = "{} lance un dé... ".format(user)
	dice = randint(1,6)
	if dice == 1:
		msg += "1... ça valait le coup de me déranger pour ça ?"
	elif dice == 2:
		msg += "2... pas de chance... tu payes ta tournée ?"
	elif dice == 3:
		msg += "3 ! Tout juste la moyenne !"
	elif dice == 4:
		msg += "4 ! pas mal, mais pas extra non plus.. Comme ta maman au lit MrDestructoid"
	elif dice == 5:
		msg += "5 ! t'aurais pas triché par hasard ?"
	elif dice == 6 : 
		msg += "6 ! Tu remportes une renault twingo d'occas' ou une magnifique encyclopédie faune marine de 1996, au choix ! Bravo !"
	return [msg]

def arg(user, arg):
	phrases=["Sept.","TheIlluminati  illumimimathy TheIlluminati ","#Incomming","Combien faut-il de nains pour creuser un tunnel de 28m dans du granite ?","Je suis la main du roi ? Allô ?","MONSTER OLD Keepo","C'est vraiment nainportequoi cette histoire...","<3 AlexMog et Diabalzane <3","RIP Andromeda, tu étais l'amour de ma vie MrDestructoid","Eric... traitre...","Les points ça se relie pas tout seuls hein.. Pour ça faut demander à Boborto et t0t0k ;)","ARG ? C'est une commande plutot Unexpected...","lisez le GDOC non d'un boulon !","Leprechaun qui danse en jouant du violon sur une table basse... WTF ? Pourquoi je dis ça moi ?!","jk j'ui lhqycudj vqyj sxyuh q tushofjuh sq ? ww, j'qi bu theyj à kd !seeayu !"]
	return [phrases[randint(0,len(phrases)-1)]]

def commu(user, arg):
	return ["Venez sur le discord de La Commu Unexpected ! https://discord.gg/UCkPMe9"]

def bite(user, arg):
	return ["La taille de la bite de {} est 8{}D".format(user, randint(1,15)*"=")]

def tog(user, arg):
	h = strftime("%H")
	m = strftime("%M")
	s = strftime("%S")
	tog = (int(h)+int(m)/60+int(s)/3600)/28
	print(tog)
	return ["Il est actuellement {} tog".format(round(tog,3))]

def cookie(user, arg):
	if arg.lower() == BOT_NAME.lower():
		return ["Oh trop bien des cookies ! J'adore, merci <3 <3 <3"]
	elif arg.lower() == "all":
		return ["Pluie de cookies de la part de {} ! Envoyez lui votre amour !".format(user)]
	elif arg.lower() == user:
		return ["{} mange un cookie tout seul dans son coin... volez lui !".format(user)]
	elif isViewer(arg.lower()):
		return ["{} offre un cookie à {}... belle preuve d'amour <3".format(user,arg)]
	else:
		return notViewer(user,arg)