'''
    @totok (twitter.com/redtotok)
	project botT0k - ask me before using my code please
	made with Twitch-API : https://github.com/justintv/Twitch-API/blob/master/IRC.md

	you may need install 'requests' libraries : http://docs.python-requests.org/en/master/user/install/#install

	commands :
	- returning lists from files
	- updating files from real time Twitch lists
'''
import requests
from settings import *

PATH_COMMAND_LIST = "./lists/commands"
PATH_ADMINS_LIST = "./lists/admins"
PATH_VIEWERS_LIST = "./lists/viewers"

def readFile(path):
	file = open(path,'r')
	tab = []
	for line in file:
		if line[0] != "#" and line[0] != "\n":
			tab.append(line[:len(line)-1])
	file.close()
	return tab

def viewerList():
	global CHANNEL
	url = "https://tmi.twitch.tv/group/user/{}/chatters".format(CHANNEL[1:])
	response = requests.get(url)
	jsonResponse = response.json()

	viewerList = jsonResponse['chatters']['moderators']
	viewerList += jsonResponse['chatters']['staff']
	viewerList += jsonResponse['chatters']['admins']
	viewerList += jsonResponse['chatters']['global_mods']
	viewerList += jsonResponse['chatters']['viewers']

	tab = readFile(PATH_VIEWERS_LIST)

	tempTab = tab

	file = open(PATH_VIEWERS_LIST,'a')
	for viewer in viewerList:
		if viewer not in tab:
			tab.append(viewer)
			file.write(viewer+"\n")
	file.close()

	return tab

def getList(listName):
	if listName == 'commands':
		return readFile(PATH_COMMAND_LIST)
	elif listName == 'admins':
		return readFile(PATH_ADMINS_LIST)
	elif listName == 'viewers':
		return viewerList()
	else:
		return -1
