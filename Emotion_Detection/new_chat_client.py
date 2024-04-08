import socket
import threading
import kivy
from kivy.app import App
from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
#kivy.require("1.9.0")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class BoxLayoutForCHAT(BoxLayout):  #boxlayout
    def __init__(self):
        super(BoxLayoutForCHAT, self).__init__()

    def connect_to_server(self):
        if self.nickname_text.text != "":
            client.connect((self.ip_text.text, 9999))
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                print("i am here, because message received is NICK")
                self.chat_text.text += "You have joined the chat room"+"\n"
                client.send(self.nickname_text.text.encode('utf-8'))
                self.send_btn.disabled = False
                self.message_text.disabled = False
                self.connect_btn.disabled = True
                self.ip_text.disabled = True

                self.make_invisiable(self.connection_grid)
                self.make_invisiable(self.connect_btn)
                thread = threading.Thread(target = self.receive)
                thread.start()
    def make_invisiable(self, widget):
        widget.visible = False
        widget.size_hint_x = None
        widget.size_hint_y = None
        widget.height = 0
        widget.width = 0
        widget.text = ""
        widget.opacity = 0


    def send_message(self):
        #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = self.nickname_text.text+": "+self.message_text.text
        client.send(s.encode('utf-8'))
    def receive(self):
        stop = False
        print("inside receive function")
        while not stop:
             try:
                print("before reading message")
                message = client.recv(4096)
                print("after reading message")
                message = message.decode('utf-8')
                print("message : ",message)
                print("type(message) = ", type(message))
                print("self.chat_text.text : ",self.chat_text.text)
                print("type(self.chat_text.text) = ", type(self.chat_text.text))
                str1 = str(self.chat_text.text)
                str2 = str(str(message)+"\n")
                s = str(str1 + str2)
                print("s : ",s)
                self.updater(s)
                print("last line of try block")
             except:
                print("inside except block")
                print("ERROR")
                client.close()
                stop = True
    @mainthread
    def updater(self, s):
        self.chat_text.text = s

class new_chat_client(App):
    def build(self):
        return BoxLayoutForCHAT()


new_chat_client = new_chat_client()
new_chat_client.run()