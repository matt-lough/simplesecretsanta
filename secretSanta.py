#secretSanta.py
##
# Generate pairings from either JSON or XML listings of usernames
# and email addresses, then sends them an email with their secret
# santa.
##
# - sifRAWR -
# Last updated 29/10/2012
##
# CONFIG
##
USE_PRICE = 1
# 1 = Max price will be in email
# 0 = No max price mentioned
MAX_PRICE = 10
# The maximum price in dollars
EMAIL_USER = 'santa_emailer'
# The user part of your email address
EMAIL_PASSWORD = 's3cr3t'
# The emails password
##

import random
import smtplib  
import json
import xml.etree.ElementTree as ET

class SecretSanta:
	"""
	Generates pairings for the secret santa and sends them emails.
	"""
	def __init__(self, file_name):
		self.username = EMAIL_USER
		self.password = EMAIL_PASSWORD 
		self.fromaddr = EMAIL_USER + '@gmail.com'
		if file_name.split('.')[1] == 'json':
			self.candidates = self.getCandidatesJSON(file_name)
		elif file_name.split('.')[1] == 'xml':
			self.candidates = self.getCandidatesXML(file_name)
		else:
			print "ERROR\nYou provided an unsupported file format.\nUse .json or .xml!"
			raise SystemExit(0)
		self.connectEmailServer()
		self.visited = []
			
	def lenCandidates(self):
		return len(self.candidates)

	def connectEmailServer(self):
		self.server = smtplib.SMTP('smtp.gmail.com:587')
		self.server.starttls()  
		self.server.login(self.username, self.password)
		
	def sendMail(self, name, recipName, recipAddr):
		price_msg = 'Make sure they are $' + str(MAX_PRICE) + ' or less.'
		msg = 'Hi ' + name + '\r\nYour secret santa is ' + recipName + \
			  '.\r\nGifts will be exchanged on the 22nd of December. ' + \
			  (price_msg if USE_PRICE else '') + '\r\nHave fun!\r\n'
		headers = ["From: " + EMAIL_USER + '@gmail.com',
				   "Subject: " + "Secret Santa!",
				   "To: " + recipAddr,
				   "MIME-Version: 1.0",
				   "Content-Type: text/plain"]
		headers = "\r\n".join(headers)
		self.server.sendmail(EMAIL_USER + "@gmail.com", recipAddr, headers + "\r\n\r\n" + msg)
		print "Email sent to " + recipAddr
		
	def chooseCandidate(self):
		personKey = random.choice(self.candidates.keys())
		while personKey in self.visited:
			 personKey = random.choice(self.candidates.keys())
		self.visited.append(personKey)
		return personKey
		
	def candidatesAddr(self, name):
		return self.candidates[name]
		
	def cleanup(self):
		self.server.quit()  
		print "Completed."
		
	def getCandidatesJSON(self, file_name):
		ret_candidates = {}
		with open(file_name) as f:
			json_list = json.load(f)
		for d in json_list:
			cur_pair = d.values()
			ret_candidates[cur_pair[0]] = cur_pair[1]
		return ret_candidates
		
	def getCandidatesXML(self, file_name):
		ret_candidates = {}
		tree = ET.parse(file_name)
		root = tree.getroot()
		for child in root:
			ret_candidates[child[0].text] = child[1].text
		return ret_candidates
		
def run():
	santa = SecretSanta('emails.xml')
	start = santa.chooseCandidate()
	prev = start
	start = [start, santa.candidatesAddr(start)]
	logfile = open('santa.log','w')
	for i in range(santa.lenCandidates() - 1):
		next = santa.chooseCandidate()
		santa.sendMail(prev, next, santa.candidatesAddr(prev))
		logfile.write(prev + ' -> ' + next + '\n')
		prev = next
	santa.sendMail(prev, start[0], santa.candidatesAddr(prev))  
	logfile.write(prev + ' -> ' + start[0] + '\n')
	logfile.close()
	santa.cleanup()

if __name__ == '__main__':
    run()