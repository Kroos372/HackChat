import json, websocket, ssl

class HackChat:
    def __init__(self, channel: str, nick: str, passwd: str="", color: str=""):
        self.onlineUsers = []
        self.channel = channel
        self.nick = nick
        self.passwd = passwd
        self.ws = websocket.create_connection("wss://hack.chat/chat-ws", sslopt={"cert_reqs": ssl.CERT_NONE})
        self._sendPacket({"cmd": "join", "channel": channel, "nick": nick, "password": passwd})
        if color: self.changeColor(color)

    def _sendPacket(self, packet: dict):
        encoded = json.dumps(packet)
        self.ws.send(encoded)

    def sendMsg(self, msg: str):
        self._sendPacket({"cmd": "chat", "text": msg})

    def sendWhisper(self, to: str, msg: str):
        self._sendPacket({"cmd": "whisper", "nick": to, "text": msg})

    def sendEmote(self, msg: str):
        self._sendPacket({"cmd": "emote", "text": msg})

    def changeColor(self, color: str):
        self._sendPacket({"cmd": "changecolor", "color": color})

    def changeNick(self, nick: str):
        self._sendPacket({"cmd": "changenick", "nick": nick})
        self.nick = nick

    def invite(self, nick: str, channel: str):
        self._sendPacket({"cmd": "invite", "nick": nick, "channel": channel})

    def onJoin(self, joiner: str, hash_: str, trip: str):
        self.onlineUsers.append(joiner)

    def onLeave(self, lefter: str):
        self.onlineUsers.remove(lefter)

    def onColorChange(self, sender: str, color: str, trip: str):
        pass

    def onEmote(self, sender: str, msg: str):
        if sender == self.nick: return

    def onSet(self, nicks: list, users: list):
        self.onlineUsers = nicks

    def onWhisper(self, sender: str, msg: str):
        if isinstance(sender, int) or sender == self.nick: return

    def onInvite(self, sender: str, channel: str):
        if not sender or sender == self.nick: return

    def onMessage(self, sender: str, msg: str, trip: str):
        if sender == self.nick: return

    def run(self):
        while True:
            result = json.loads(self.ws.recv())
            cmd = result["cmd"]
            type_ = result.get("type")

            # 接收到消息
            if cmd == "chat":
                self.onMessage(result["nick"], result["text"], result.get("trip", ""))
            # 有人加入
            elif cmd == "onlineAdd":
                self.onJoin(result["nick"], result["hash"], result.get("trip", ""))
            # 有人离开
            elif cmd == "onlineRemove":
                self.onLeave(result["nick"])
            # 改变颜色
            elif cmd == "updateUser":
                self.onColorChange(result["nick"], result["color"], result.get("trip", ""))
            # Emote
            elif cmd == "emote":
                self.onEmote(result["nick"], " ".join(result["text"].split(" ")[1:]))
            # 接收到私信
            elif type_ == "whisper":
                self.onWhisper(result["from"], ": ".join(result["text"].split(": ")[1:]))
            # 被人邀请
            elif type_ == "invite":
                self.onInvite(result["from"], result["inviteChannel"])
            # 警告信息
            elif cmd == "warn":
                print("Warn: ", result["text"])
            # 提示信息
            elif cmd == "info":
                print("Info: ", result["text"])
            # 当前在线用户
            elif cmd == "onlineSet":
                self.onSet(result["nicks"], result["users"])

if __name__ == "__main__":
    print("我只是一个库，不要运行我捏~")