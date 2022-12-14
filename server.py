import socket
import threading
import pickle
import os
import sys
import random
import numpy as np
import time

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
		self.turnList.remove(username)
		print(self.turnList)
	
	def connect(self,username,client):
		self.turnList.append(username)
		self.onlineMembers.add(username)
		self.clients[username] = client


	def sendMessage(self,message,username):
		for member in self.onlineMembers:
			if member != username:
				message_to_send = username +": "+ message
				message_to_send = message_to_send.encode("UTF-8")
				self.clients[member].send(len(message_to_send).to_bytes(2, byteorder='big'))
				self.clients[member].send(message_to_send)

	def listToString(self,s):   
		str1 = ""
		for ele in s:
			if(str1 == ""):
				str1 += str(ele)
			else:
				str1 += "," + str(ele)
		return str1

	def showPiles(self, username):
		if(len(self.pile1) > 0):
			toSend = "Pile 1: " + str(self.pile1[len(self.pile1) - 1]) + " - Necesita un: " + str(len(self.pile1)+1) + "\n"
		else:
			toSend = "Pile 1: null\n"
		if(len(self.pile2) > 0):
			toSend += "Pile 2: " + str(self.pile2[len(self.pile2) - 1]) + " - Necesita un: " + str(len(self.pile2)+1) + "\n"
		else:
			toSend += "Pile 2: null\n"
		if(len(self.pile3) > 0):
			toSend += "Pile 3: " + str(self.pile3[len(self.pile3) - 1]) + " - Necesita un: " + str(len(self.pile3)+1) + "\n"
		else:
			toSend += "Pile 3: null\n"
		if(len(self.pile4) > 0):
			toSend += "Pile 4: " + str(self.pile4[len(self.pile4) - 1]) + " - Necesita un: " + str(len(self.pile4)+1) + "\n"
		else:
			toSend += "Pile 4: null\n"

		message_to_send = toSend.encode("UTF-8")
		self.clients[username].send(len(message_to_send).to_bytes(2, byteorder='big'))
		self.clients[username].send(message_to_send)



	def startDeck(self):
		
		random.shuffle(self.turnList)
		random.shuffle(self.mainDeck)
		self.userTurn = len(self.turnList) - 1
		for member in self.onlineMembers:	
			print(self.clients[member])
			arrSend = []
			for i in range(20):
				arrSend.append(self.mainDeck.pop(0))
			strSend = self.listToString(arrSend)
			print(self.turnList)
			message_to_send = strSend.encode("UTF-8")
			self.clients[member].send(len(message_to_send).to_bytes(2, byteorder='big'))
			self.clients[member].send(message_to_send)

			message_to_send = "Es el turno de: " + self.turnList[self.userTurn] + "\n Usar /turn:accion:cardFrom-card:cardTo para mover cartas (descartar/poner en pila) \n Use /help para ver acciones"
			message_to_send = message_to_send.encode("UTF-8")
			self.clients[member].send(len(message_to_send).to_bytes(2, byteorder='big'))
			self.clients[member].send(message_to_send)
		

	def resetPile(self, pile):
		for i in range(len(pile)):
			self.mainDeck.append(pile.pop())
		random.shuffle(self.mainDeck)
			
	def addToPile(self, card, pile):
		try:
			if pile == "1":
				if(len(self.pile1) == 0 and (card == "1" or card == "99")):
					self.pile1.append(card)
					return "Carta a??adida"
				elif ((len(self.pile1) == 11) and (card == "12" or card == "99")):
						self.resetPile(self.pile1)
						return "Carta a??adida"
				elif((len(self.pile1) > 0) and (len(self.pile1) + 1 == int(card)) or card == "99"):
					self.pile1.append(card)
					return "Carta a??adida"
				else:
					return "Movida Invalida"
			elif pile == "2":
				if(len(self.pile2) == 0 and (card == "1" or card == "99")):
					self.pile2.append(card)
					return "Carta a??adida"
				elif ((len(self.pile2) == 11) and (card == "12" or card == "99")):
					self.resetPile(self.pile2)
					return "Carta a??adida"
				elif((len(self.pile2) > 0) and (len(self.pile2) + 1 == int(card)) or card == "99"):
					self.pile2.append(card)
					return "Carta a??adida"
				else:
					return "Movida Invalida"
			elif pile == "3":
				if(len(self.pile3) == 0 and (card == "1" or card == "99")):
					self.pile3.append(card)
					return "Carta a??adida"
				elif ((len(self.pile3) == 11) and (card == "12" or card == "99")):
					self.resetPile(self.pile3)
					return "Carta a??adida"
				elif((len(self.pile3) > 0) and (len(self.pile3) + 1 == int(card)) or card == "99"):
					self.pile3.append(card)
					return "Carta a??adida"
				else:
					return "Movida Invalida"
			elif pile == "4":
				if(len(self.pile4) == 0 and (card == "1" or card == "99")):
					self.pile4.append(card)
					return "Carta a??adida"
				elif ((len(self.pile4) == 11) and (card == "12" or card == "99")):
					self.resetPile(self.pile4)
					return "Carta a??adida"
				elif((len(self.pile4) > 0) and (len(self.pile4) + 1 == int(card)) or card == "99"):
					self.pile4.append(card)
					return "Carta a??adida"
				else:
					return "Movida Invalida"
		except:
			return "Movida Invalida"
		return "Movida Invalida"

	def sendHandCards(self, user):
			
			message_to_send = "/handSize".encode("UTF-8")
			self.clients[user].send(len(message_to_send).to_bytes(2, byteorder='big'))
			self.clients[user].send(message_to_send)

			length_of_message = int.from_bytes(self.clients[user].recv(2), byteorder='big')
			handSize = self.clients[user].recv(length_of_message).decode("UTF-8")

			sendCards = []
			print(handSize)
			for i in range (5 - int(handSize)):
				sendCards.append(self.mainDeck.pop(0))
			message_to_send = self.listToString(sendCards).encode("UTF-8")
			self.clients[user].send(len(message_to_send).to_bytes(2, byteorder='big'))
			self.clients[user].send(message_to_send)


	def endTurn(self):
		if(len(self.onlineMembers) - 1 <= 0):
			self.userTurn = len(self.onlineMembers) - 1
			for member in self.onlineMembers:
				message_to_send = "Es el turno de: " + self.turnList[self.userTurn]
				message_to_send = message_to_send.encode("UTF-8")
				self.clients[member].send(len(message_to_send).to_bytes(2, byteorder='big'))
				self.clients[member].send(message_to_send)
					
		else:
			self.userTurn = self.userTurn-1
			for member in self.onlineMembers:
				message_to_send = "Es el turno de: " + self.turnList[self.userTurn]
				message_to_send = message_to_send.encode("UTF-8")
				self.clients[member].send(len(message_to_send).to_bytes(2, byteorder='big'))
				self.clients[member].send(message_to_send)

	def removeTop(self, username):
		message_to_send = "/removeLastTop".encode("UTF-8")
		self.clients[username].send(len(message_to_send).to_bytes(2, byteorder='big'))
		self.clients[username].send(message_to_send)

	def turn(self,msg,username):
		try:
			parts = msg.split(":")
			sendStatus = self.addToPile(parts[1],parts[2])
			if(sendStatus != "Movida Invalida"):
				message_to_send = sendStatus.encode("UTF-8")
				self.clients[username].send(len(message_to_send).to_bytes(2, byteorder='big'))
				self.clients[username].send(message_to_send)
				self.showPiles(username)
				self.removeTop(username)
			else:
				message_to_send = sendStatus.encode("UTF-8")
				self.clients[username].send(len(message_to_send).to_bytes(2, byteorder='big'))
				self.clients[username].send(message_to_send)
		except:
			message_to_send = "Movida Invalida".encode("UTF-8")
			self.clients[username].send(len(message_to_send).to_bytes(2, byteorder='big'))
			self.clients[username].send(message_to_send)

		
			
				

def pyconChat(client, username, groupname):
	while True:
		length_of_message = int.from_bytes(client.recv(2), byteorder='big')
		msg = client.recv(length_of_message).decode("UTF-8")
		if msg == "/viewRequests":
			client.recv(1024).decode("utf-8")
			if username == groups[groupname].admin:
				client.recv(1024)
				message_to_send = pickle.dumps(groups[groupname].joinRequests).encode("UTF-8")
				client.send(len(message_to_send).to_bytes(2, byteorder='big'))
				client.send(message_to_send)
			else:
				message_to_send = "No es admin".encode("UTF-8")
				client.send(len(message_to_send).to_bytes(2, byteorder='big'))
				client.send(message_to_send)
		elif msg == "/approveRequest":
			if username == groups[groupname].admin:
				length_of_message = int.from_bytes(client.recv(2), byteorder='big')
				usernameToApprove = client.recv(length_of_message).decode("UTF-8")
				if usernameToApprove in groups[groupname].joinRequests:
					groups[groupname].joinRequests.remove(usernameToApprove)
					groups[groupname].allMembers.add(usernameToApprove)
					if usernameToApprove in groups[groupname].waitClients:
						groups[groupname].connect(usernameToApprove,groups[groupname].waitClients[usernameToApprove])
						del groups[groupname].waitClients[usernameToApprove]
					print("Member Approved:",usernameToApprove,"| Lobby:",groupname)
					message_to_send = "Solicitud Aceptada".encode("UTF-8")
					client.send(len(message_to_send).to_bytes(2, byteorder='big'))
					client.send(message_to_send)
					
				else:
					message_to_send = "Usuario Invalido".encode("UTF-8")
					client.send(len(message_to_send).to_bytes(2, byteorder='big'))
					client.send(message_to_send)
			else:
				message_to_send = "No es admin".encode("UTF-8")
				client.send(len(message_to_send).to_bytes(2, byteorder='big'))
				client.send(message_to_send)
		elif msg == "/disconnect":
			groups[groupname].disconnect(username)
			print("User Disconnected:",username,"| Group:",groupname)
			break
		elif (msg == "/startGame" and username == groups[groupname].admin):
			groups[groupname].startDeck()
			print("Game Start")
		elif(("/turn" in msg) and username == groups[groupname].turnList[groups[groupname].userTurn]):
			groups[groupname].turn(msg, username)
		elif(msg == "/help"):
			help = "Acciones: \nx)discard:X:X \nx)toPile \nx)seeCards \nx)sendHand \nx)serverPiles \n-----------\ncardFrom validos: \nx)deck \nx)hand-X \nx)pile-X \n-----------\ncardTo validos: \nx)pile-X"
			message_to_send = help.encode("UTF-8")
			client.send(len(message_to_send).to_bytes(2, byteorder='big'))
			client.send(message_to_send)
		elif(msg == "/sendHand" and username == groups[groupname].turnList[groups[groupname].userTurn]):
			groups[groupname].sendHandCards(username)
		elif(msg == "/endTurn"):
			groups[groupname].endTurn()
		elif(msg == "/serverPiles"):
			groups[groupname].showPiles(username)
		elif(msg == "/playerWin"):
			winner = "El ganador es : " + username + "!!!!!!!!"
			groups[groupname].sendMessage(winner, "Server")
			break
			
		else:
    			groups[groupname].sendMessage(msg,username)


def handshake(client):
	length_of_message = int.from_bytes(client.recv(2), byteorder='big')
	username = client.recv(length_of_message).decode("UTF-8")

	#message_to_send = "bye".encode("UTF-8")
	#client.send(len(message_to_send).to_bytes(2, byteorder='big'))
	#client.send(message_to_send)

	length_of_message = int.from_bytes(client.recv(2), byteorder='big')
	groupname = client.recv(1024).decode("utf-8")
	if groupname in groups:
		if username in groups[groupname].allMembers:
			groups[groupname].connect(username,client)
			print("User Connected:",username,"| Group:",groupname)
		else:
			groups[groupname].joinRequests.add(username)
			groups[groupname].waitClients[username] = client
			print("Join Request:",username,"| Group:",groupname)
		threading.Thread(target=pyconChat, args=(client, username, groupname,)).start()
	else:
		groups[groupname] = Group(username,client)
		groups[groupname].turnList.append(username)
		threading.Thread(target=pyconChat, args=(client, username, groupname,)).start()
		print("New Group:",groupname,"| Admin:",username)

def main():

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