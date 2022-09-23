import socket
import threading
import pickle
import os
import sys
import random
import numpy as np

groups = {}
fileTransferCondition = threading.Condition()

class Group:
	def __init__(self,admin,client):
		self.admin = admin
		self.clients = {}
		self.offlineMessages = {}
		self.allMembers = set()
		self.onlineMembers = set()
		self.joinRequests = set()
		self.waitClients = {}
		self.mainDeck = [1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,]
		self.pile1 = []
		self.pile2 = []
		self.pile3 = []
		self.pile4 = []
		self.turnList =[]
		self.userTurn = 0

		self.clients[admin] = client
		self.allMembers.add(admin)
		self.onlineMembers.add(admin)

	def disconnect(self,username):
		self.onlineMembers.remove(username)
		del self.clients[username]
	
	def connect(self,username,client):
		self.turnList.append(username)
		self.onlineMembers.add(username)
		self.clients[username] = client


	def sendMessage(self,message,username):
		for member in self.onlineMembers:
			if member != username:
				self.clients[member].send(bytes(username + ": " + message,"utf-8"))

	def listToString(self,s):   
		str1 = ""
		for ele in s:
			if(str1 == ""):
				str1 += str(ele)
			else:
				str1 += "," + str(ele)
		return str1

	def startDeck(self):
		random.shuffle(self.turnList)
		random.shuffle(self.mainDeck)
		self.userTurn = len(self.turnList)
		for member in self.onlineMembers:	
			arrSend = []
			for i in range(20):
				arrSend.append(self.mainDeck.pop(0))
			print(arrSend,len(self.mainDeck))
			self.clients[member].send(bytes(self.listToString(arrSend),'utf-8'))
		print(self.onlineMembers)

	def resetPile(self, pile):
		for i in range(11):
			self.mainDeck.append(pile.pop(i))
			random.shuffle(self.mainDeck)
			
	def addToPile(self, card, pile):
		if pile == "1":
			if (self.pile1[len(self.pile1) - 1] == 11 and card == 12):
					self.resetPile(self.pile1)
			elif(self.pile1[len(self.pile1) - 1] + 1 == card):
				self.pile1.append(card)
			else:
				return "Invalid Move"
		elif pile == "2":
			if (self.pile2[len(self.pile2) - 1] == 11 and card == 12):
				self.resetPile(self.pile2)
			elif(self.pile2[len(self.pile2) - 1] + 1 == card):
				self.pile2.append(card)
			else:
				return "Invalid Move"
		elif pile == "3":
			if (self.pile3[len(self.pile3) - 1] == 11 and card == 12):
				self.resetPile(self.pile3)
			elif(self.pile3[len(self.pile3) - 1] + 1 == card):
				self.pile3.append(card)
			else:
				return "Invalid Move"
		elif pile == "4":
			if (self.pile4[len(self.pile4) - 1] == 11 and card == 12):
				self.resetPile(self.pile4)
			elif(self.pile4[len(self.pile4) - 1] + 1 == card):
				self.pile4.append(card)
			else:
				return "Invalid Move"

	def sendHandCards(self, handSize, user):
		sendCards = []
		for i in range (5 - handSize):
			sendCards.append(self.mainDeck.pop(0))
		self.clients[user].send(bytes(self.listToString(sendCards),'utf-8'))

	def resetTurn(self):
		self.userTurn = len(self.onlineMembers)

	def turn(self,user,msg):
		if(user == self.turnList[self.userTurn]):
			if(msg == "addPile"):
    				pass
    		

		
    		

				

def pyconChat(client, username, groupname):
	while True:
		msg = client.recv(1024).decode("utf-8")
		if msg == "/viewRequests":
			client.send(b"/viewRequests")
			client.recv(1024).decode("utf-8")
			if username == groups[groupname].admin:
				client.send(b"/sendingData")
				client.recv(1024)
				client.send(pickle.dumps(groups[groupname].joinRequests))
			else:
				client.send(b"You're not an admin.")
		elif msg == "/approveRequest":
			client.send(b"/approveRequest")
			client.recv(1024).decode("utf-8")
			if username == groups[groupname].admin:
				client.send(b"/proceed")
				usernameToApprove = client.recv(1024).decode("utf-8")
				if usernameToApprove in groups[groupname].joinRequests:
					groups[groupname].joinRequests.remove(usernameToApprove)
					groups[groupname].allMembers.add(usernameToApprove)
					if usernameToApprove in groups[groupname].waitClients:
						groups[groupname].waitClients[usernameToApprove].send(b"/accepted")
						groups[groupname].connect(usernameToApprove,groups[groupname].waitClients[usernameToApprove])
						del groups[groupname].waitClients[usernameToApprove]
					print("Member Approved:",usernameToApprove,"| Lobby:",groupname)
					client.send(b"User has been added to the lobby.")
					
				else:
					client.send(b"The user has not requested to join.")
			else:
				client.send(b"You're not an admin.")
		elif msg == "/disconnect":
			client.send(b"/disconnect")
			client.recv(1024).decode("utf-8")
			groups[groupname].disconnect(username)
			print("User Disconnected:",username,"| Group:",groupname)
			break
		elif msg == "/messageSend":
			client.send(b"/messageSend")
			message = client.recv(1024).decode("utf-8")
			groups[groupname].sendMessage(message,username)
		elif msg == "/waitDisconnect":
			client.send(b"/waitDisconnect")
			del groups[groupname].waitClients[username]
			print("Waiting Client:",username,"Disconnected")
			break
		elif msg == "/onlineMembers":
			client.send(b"/onlineMembers")
			client.recv(1024).decode("utf-8")
			client.send(pickle.dumps(groups[groupname].onlineMembers))
		elif (msg == "/startGame" and username == groups[groupname].admin):
			groups[groupname].startDeck()
			print("Game Start")
		else:
			print("UNIDENTIFIED COMMAND:",msg)


def handshake(client):
	username = client.recv(1024).decode("utf-8")
	client.send(b"/sendGroupname")
	groupname = client.recv(1024).decode("utf-8")
	if groupname in groups:
		if username in groups[groupname].allMembers:
			groups[groupname].connect(username,client)
			client.send(b"/ready")
			print("User Connected:",username,"| Group:",groupname)
		else:
			groups[groupname].joinRequests.add(username)
			groups[groupname].waitClients[username] = client
			groups[groupname].sendMessage(username+" has requested to join the group.","PyconChat")
			client.send(b"/wait")
			print("Join Request:",username,"| Group:",groupname)
		threading.Thread(target=pyconChat, args=(client, username, groupname,)).start()
	else:
		groups[groupname] = Group(username,client)
		threading.Thread(target=pyconChat, args=(client, username, groupname,)).start()
		client.send(b"/adminReady")
		print("New Group:",groupname,"| Admin:",username)

def main():
	''' if len(sys.argv) < 3:
		print("USAGE: python server.py <IP> <Port>")
		print("EXAMPLE: python server.py localhost 8000")
		return '''
	listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#listenSocket.bind((sys.argv[1], int(sys.argv[2])))
	listenSocket.bind(("localhost", int(8000)))
	listenSocket.listen(10)
	print("PyconChat Server running")
	while True:
		client,_ = listenSocket.accept()
		threading.Thread(target=handshake, args=(client,)).start()

if __name__ == "__main__":
	main()