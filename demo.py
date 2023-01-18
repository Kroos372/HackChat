from HackChat import HackChat

class MyChat(HackChat):
	def onMessage(self, sender, msg, trip):
		super().onMessage(sender, msg, trip)
		if msg == "hi":
			self.sendMsg(f"Hi, {sender}!")
	def onJoin(self, joiner, hash_, trip):
		super().onJoin(sender, joiner, hash_, trip)
		self.sendMsg(f"Welcome, {joiner}!")
		self.sendWhisper(f"Quickly run!!!")

if __name__ == '__main__':
	obj = MyChat("test", "MyBot", "NoPassword")

	obj.run()