import threading
from random import random
import random

import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np


import kivy
from PIL.Image import Image
from kivy.clock import mainthread
from kivy.core.text import Text
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.app import App
from kivy.atlas import CoreImage
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import NumericProperty, Clock, StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.uix.widget import Widget
import matplotlib.pyplot as plt
import matplotlib
import sys
import io
kivy.require('2.0.0')

#=======================================================================================================================
import socket

from kivymd.uix.filemanager import MDFileManager

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
#SERVER = "192.168.1.12"  #belkin
SERVER = "192.168.165.141"  #vidhyarthi

ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNEXT_MSG = '!DISCONNECT'
CREATE_ACC_MSG = '!new'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)
print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
def send(msg)->bool:
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    #print(send_length)
    #print(message)
    client.send(send_length)
    client.send(message)
    incoming_msg = client.recv(64)
    incoming_msg = incoming_msg.decode(FORMAT)
    incoming_msg = True if incoming_msg=="True" else False
    return incoming_msg
#=======================================================================================================================


class MainWindow(Screen):
    pass

class FirstWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class BoxLayoutForCHAT(BoxLayout):  #boxlayout
    chat_client = None
    def __init__(self, size):
        super(BoxLayoutForCHAT, self).__init__()
        self.chat_client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def get_client(self):
        return self.chat_client
    def connect_to_server(self):
        self.chat_client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("inside connect with server function")
        if self.nickname_text.text != "":
            print("inside first if")
            print("before creating self.chat_client")
            print("server ip address is",self.ip_text.text)
            self.chat_client.connect((self.ip_text.text, 9999))
            print("after creating self.chat_client")
            print("before receiving message")
            message = self.chat_client.recv(1024).decode('utf-8')
            print("after receiving message")
            if message == "NICK":
                print("- inside 'NICK' if statement")
                print("i am here, because message received is NICK")
                self.chat_text.text += "You have joined the chat room"+"\n"
                self.chat_client.send(self.nickname_text.text.encode('utf-8'))
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
        self.chat_client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_client.connect((self.ip_text.text, 9999))
        #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("inside send message function")
        print("before s")
        s = self.nickname_text.text+": "+self.message_text.text +"\n"
        print("s = ",s)
        print(self.chat_client)
        #MainWidget.update_chat_messages(MainWidget(), s)
        self.updater(s)
        self.chat_client.send(s.encode('utf-8'))
        print("last line of send message function")
    # @mainthread
    # def helper_main_thread_send_message(self,s):
    #     self.chat_client.send(s.encode('utf-8'))
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
                self.chat_client.close()
                stop = True
    @mainthread
    def updater(self, s):
        self.chat_text.text += s


class MainWidget(Widget):
    path = ""
    sign_in_button = []
    s_width = NumericProperty(Window.size[0])
    s_height = NumericProperty(Window.size[1])
    signin_window = None
    popup = None
    extra_popup = None
    layout = None
    layout1 = None
    layout_graph = None
    extra_graph_popup = None
    chat_popup = None
    emotion_popup = None
    survey_popup = None
    feel_better_popup = None
    chat_window_instance = None
    close_chat = None
    buttons = []
    tx1=None
    tx2=None
    entity_label = ""
    graph_label = ""
    entity = None
    signed_in = False
    entered_id = -1
    layout_chat = None
    layout_survey = None
    bt1=None
    bt2 = None

    client = None
    round_corners3 = []
    round_corners2 = []
    round_corners4 = []
    round_corners1 = []

    file_manager_obj= None
    err_popup1 = None
    err_popup2 = None
    survey_button = []



    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        client.connect(ADDR)
        self.file_manager_obj = MDFileManager(
            select_path=self.select_path,
            #exit_manager=self.exit_manager,
            #preview=True,
            search = "all"
        )
        self.client = client
        with self.canvas:
            self.client = client
            self.init_signin_button()
            self.init_survey_button()
            self.init_buttons()

    def on_signin_press(self, widget):
        self.open_popup_window()

    def open_popup_window(self):
        layout = GridLayout(cols=1)
        self.txt1 = TextInput(text='user-id', multiline=False, write_tab=False)
        layout.add_widget(self.txt1)
        self.txt2 = TextInput(text='password', multiline=False, write_tab = False)
        layout.add_widget(self.txt2)
        submit_button = Button(text="submit", size_hint=(0.2, 0.4), pos_hint={"center_x": 0.2, "center_y": 0.2}, on_press = \
            self.submit_credentials)
        register_button = Button(text="Don't have an account?...click here", size_hint=(0.2, 0.4), pos_hint={"center_x": 0.2, "center_y": 0.2}, on_press = \
            self.register)
        button = Button(text="close", size_hint=(0.2, 0.4), pos_hint={"center_x": 0.2, "center_y": 0.2}, on_press = \
            self.close_popup_window)
        layout.add_widget(submit_button)
        layout.add_widget(register_button)
        #layout.add_widget(label)
        layout.add_widget(button)
        self.popup = Popup(title="Sign-In", content=layout, size_hint=(None, None), size=(400, 400), auto_dismiss=False)
        self.popup.open()


    def submit_credentials(self, widget):
        if self.txt1==None or self.txt2 ==None:
            #Clock.schedule_once(self.close_popup_window, 5)
            return
        else:
            str_temp = self.txt1.text + " " + self.txt2.text
            #self.client.connect(ADDR)
            result = send(str_temp)
            print("result = ",result)
            if result:
                self.popup.title = "Signed in successfully!"
                self.signed_in = True
                if self.txt1.text.startswith('d'):
                    self.entity = "doctor"
                    self.buttons[0].disabled = False
                    self.buttons[1].disabled = False
                    self.buttons[2].disabled = False
                    self.buttons[3].disabled = False
                else:
                    self.entity = "patient"
                    self.buttons[0].disabled = False
                    self.buttons[1].disabled = False
                    self.buttons[2].disabled = False
            else: self.popup.title = "Incorrect credentials"
            print("entity is a ",self.entity)
            # send(DISCONNEXT_MSG)
            #Clock.schedule_once(self.close_popup_window, 5)

    def register(self, widget):
        self.layout1 = GridLayout(cols=1)
        self.entity_label = Label(text="Choose either doctor or patient:")
        self.layout1.add_widget(self.entity_label)
        doctor_button = Button(text="Doctor", size_hint=(0.2, 0.4),pos_hint={"center_x": 0.2, "center_y": 0.2}, on_press= self.isDoctor )
        patient_button = Button(text="Patient", size_hint=(0.2, 0.4),pos_hint={"center_x": 0.2, "center_y": 0.2}, on_press= self.isPatient )
        button = Button(text="back", size_hint=(0.2, 0.4), pos_hint={"center_x": 0.2, "center_y": 0.2}, on_press= self.close_extra_popup_window)
        self.layout1.add_widget(doctor_button)
        self.layout1.add_widget(patient_button)
        self.layout1.add_widget(button)
        self.extra_popup = Popup(title="Sign-In", content=self.layout1, size_hint=(None, None), size=(400, 400), auto_dismiss=False)
        self.extra_popup.open()

        # send(DISCONNEXT_MSG)

    def isDoctor(self, widget):
        self.entity = 'doctor'
        self.signed_in = True
        self.buttons[0].disabled = False
        self.buttons[1].disabled = False
        self.buttons[2].disabled = False
        self.buttons[3].disabled = False
        print("entity is a ",self.entity)
        send("doctor")
        msg = self.client.recv(HEADER).decode(FORMAT)
        print("msg = ", msg)
        l = msg.split(" ")
        self.entity_label.text = "Generated credentials:\n\nuser id = "+l[0].strip()+"\npassword = "+l[1].strip()

    def isPatient(self, widget):
        self.entity = 'patient'
        self.signed_in = True
        self.buttons[0].disabled = False
        self.buttons[1].disabled = False
        self.buttons[2].disabled = False
        print("entity is a ",self.entity)
        send("patient")
        msg = self.client.recv(HEADER).decode(FORMAT)
        print(msg)
        l = msg.split(" ")
        self.entity_label.text = "Generated credentials:\n\nuser id = "+l[0].strip()+"\npassword = "+l[1].strip()

    def close_extra_popup_window(self, widget):
        self.extra_popup.dismiss()
        self.close_popup_window(widget)
    def close_popup_window(self, obj):
        self.popup.dismiss()

    def init_signin_button(self):
        self.sign_in_button.append(Button())
        self.sign_in_button[0].background_normal = ''
        self.sign_in_button[0].background_color = (0.68,0.35,0.23,1)
        self.sign_in_button[0].text = "Sign-In"
        self.sign_in_button[0].font_size = 25
        self.sign_in_button[0].bind(on_press= self.on_signin_press)
        self.add_widget(self.sign_in_button[0])
        x = int(self.s_width * 0.90)
        y = int(self.s_height * 0.92)
        self.sign_in_button[0].pos = [x, y]
        width = int(self.s_width * 0.08)
        height = int(self.s_height * 0.05)
        self.sign_in_button[0].width = width
        self.sign_in_button[0].height = height
        Color(0.68,0.35,0.23,1)
        r = int(width / 8)
        self.sign_in_button.append(Rectangle(pos=[x, y - r], size=[width, r]))
        self.sign_in_button.append(Rectangle(pos=[x - r, y], size=[r, height]))
        self.sign_in_button.append(Rectangle(pos=[x, y + height], size=[width, r]))
        self.sign_in_button.append(Rectangle(pos=[x + width, y], size=[r, height]))
        Color(0.68,0.35,0.23,1)
        self.sign_in_button.append(Ellipse(pos=[x - r, y - r], size=[2 * r, 2 * r]))
        self.sign_in_button.append(Ellipse(pos=[x + width - r, y - r], size=[2 * r, 2 * r]))
        self.sign_in_button.append(Ellipse(pos=[x - r, y + height - r], size=[2 * r, 2 * r]))
        self.sign_in_button.append(Ellipse(pos=[x + width - r, y + height - r], size=[2 * r, 2 * r]))

    def init_survey_button(self):
        self.survey_button.append(Button())
        self.survey_button[0].background_normal = ''
        self.survey_button[0].background_color = (0.68, 0.35, 0.23, 1)
        self.survey_button[0].text = "Take Survey"
        self.survey_button[0].font_size = 25
        self.survey_button[0].bind(on_press=self.on_survey_press)
        self.add_widget(self.survey_button[0])
        x = int(self.s_width * 0.90)
        y = int(self.s_height * 0.82)
        self.survey_button[0].pos = [x, y]
        width = int(self.s_width * 0.08)
        height = int(self.s_height * 0.05)
        self.survey_button[0].width = width
        self.survey_button[0].height = height
        Color(0.68, 0.35, 0.23, 1)
        r = int(width / 8)
        self.survey_button.append(Rectangle(pos=[x, y - r], size=[width, r]))
        self.survey_button.append(Rectangle(pos=[x - r, y], size=[r, height]))
        self.survey_button.append(Rectangle(pos=[x, y + height], size=[width, r]))
        self.survey_button.append(Rectangle(pos=[x + width, y], size=[r, height]))
        Color(0.68, 0.35, 0.23, 1)
        self.survey_button.append(Ellipse(pos=[x - r, y - r], size=[2 * r, 2 * r]))
        self.survey_button.append(Ellipse(pos=[x + width - r, y - r], size=[2 * r, 2 * r]))
        self.survey_button.append(Ellipse(pos=[x - r, y + height - r], size=[2 * r, 2 * r]))
        self.survey_button.append(Ellipse(pos=[x + width - r, y + height - r], size=[2 * r, 2 * r]))

    def on_size(self, *args):
        self.s_width, self.s_height = self.size
        self.update()

    def update_signin_button(self):
        x = int(self.s_width * 0.90)
        y = int(self.s_height * 0.92)
        self.sign_in_button[0].text = "Sign-In"
        self.sign_in_button[0].font_size = 25
        self.sign_in_button[0].pos = [x, y]
        self.sign_in_button[0].background_normal = ''
        self.sign_in_button[0].background_color = (0.68,0.35,0.23,1)
        self.sign_in_button[0].bind(on_press= self.on_signin_press)
        width = int(self.s_width * 0.08)
        height = int(self.s_height * 0.05)
        self.sign_in_button[0].width = width
        self.sign_in_button[0].height = height
        Color(0.68,0.35,0.23,1)
        r = int(width/8)
        self.sign_in_button[1].pos = [x, y-r]
        self.sign_in_button[1].size = [width, r]
        self.sign_in_button[2].pos = [x-r, y]
        self.sign_in_button[2].size = [r,height]
        self.sign_in_button[3].pos = [x, y+height]
        self.sign_in_button[3].size = [width, r]
        self.sign_in_button[4].pos = [x+width, y]
        self.sign_in_button[4].size = [r,height]
        Color(0.68,0.35,0.23,1)
        self.sign_in_button[5].pos = [x-r, y-r]
        self.sign_in_button[5].size = [2 * r, 2 * r]
        self.sign_in_button[6].pos = [x+width-r, y-r]
        self.sign_in_button[6].size = [2 * r, 2 * r]
        self.sign_in_button[7].pos = [x-r, y+height-r]
        self.sign_in_button[7].size = [2 * r, 2 * r]
        self.sign_in_button[8].pos = [x+width-r, y+height-r]
        self.sign_in_button[8].size = [2 * r, 2 * r]

    def update_survey_button(self):
        x = int(self.s_width * 0.90)
        y = int(self.s_height * 0.82)
        self.survey_button[0].text = "Take Survey"
        self.survey_button[0].font_size = 25
        self.survey_button[0].pos = [x, y]
        self.survey_button[0].background_normal = ''
        self.survey_button[0].background_color = (0.68, 0.35, 0.23, 1)
        self.survey_button[0].bind(on_press=self.on_survey_press)
        width = int(self.s_width * 0.08)
        height = int(self.s_height * 0.05)
        self.survey_button[0].width = width
        self.survey_button[0].height = height
        Color(0.68, 0.35, 0.23, 1)
        r = int(width / 8)
        self.survey_button[1].pos = [x, y - r]
        self.survey_button[1].size = [width, r]
        self.survey_button[2].pos = [x - r, y]
        self.survey_button[2].size = [r, height]
        self.survey_button[3].pos = [x, y + height]
        self.survey_button[3].size = [width, r]
        self.survey_button[4].pos = [x + width, y]
        self.survey_button[4].size = [r, height]
        Color(0.68, 0.35, 0.23, 1)
        self.survey_button[5].pos = [x - r, y - r]
        self.survey_button[5].size = [2 * r, 2 * r]
        self.survey_button[6].pos = [x + width - r, y - r]
        self.survey_button[6].size = [2 * r, 2 * r]
        self.survey_button[7].pos = [x - r, y + height - r]
        self.survey_button[7].size = [2 * r, 2 * r]
        self.survey_button[8].pos = [x + width - r, y + height - r]
        self.survey_button[8].size = [2 * r, 2 * r]

    def on_survey_press(self, widget):
        self.layout_survey = BoxLayout(orientation="vertical" ,spacing =10,)
        self.close_survey = Button(text="close",on_press = self.close_survey_popup)

        self.questions = [
            {"text": "Enter the no. of hours of sleep you get per day:", "input_type": "numeric", "range": (0, 24)},
            {"text": "Do you have frequent mood swings? (yes/no):", "input_type": "yes_no"},
            {"text": "Do you have any thoughts of self-harm? (yes/no):", "input_type": "yes_no"},
            {"text": "How many meals do you have per day:", "input_type": "numeric", "range":(0,20)},
            {"text": "Are you enjoying things right now? (yes/no):", "input_type": "yes_no"}

        ]
        self.current_question_index = 0
        self.answers = []
        self.question_label = Label(text="Enter the no. of hours of sleep you get per day:")
        self.answer_input = [TextInput( multiline= False, readonly = False, input_filter= "float" if self.questions[self.current_question_index]["input_type"] == "numeric" else None)]
        self.submit_button = Button(text="Submit",  on_press= self.submit_answer)
        self.result_label = Label( text= "")
        self.layout_survey.add_widget(self.question_label)
        self.layout_survey.add_widget(self.answer_input[0])
        self.layout_survey.add_widget(self.submit_button)
        self.layout_survey.add_widget(self.result_label)
        self.layout_survey.add_widget(self.close_survey)
        self.survey_popup = Popup(title="Take Survey", content=self.layout_survey, size=(self.s_width, self.s_height),
                                  auto_dismiss=False)
        self.survey_popup.open()
        self.update_question()

    def update_question(self):
        self.question_label.text = self.questions[self.current_question_index]["text"]
        #self.answer_input.text = ""

    def submit_answer(self, widget):
        answer = self.answer_input[-1].text
        self.layout_survey.remove_widget(self.close_survey)
        self.layout_survey.remove_widget(self.result_label)
        self.layout_survey.remove_widget(self.submit_button)
        self.layout_survey.remove_widget(self.answer_input[-1])
        self.answer_input.append(TextInput(multiline=False, readonly=False,
                                      input_filter="float" if self.questions[self.current_question_index][
                                                                  "input_type"] == "numeric" else None))
        self.submit_button = Button(text="Submit", on_press=self.submit_answer)
        self.result_label = Label(text="")
        self.close_survey = Button(text="close", on_press=self.close_survey_popup)
        self.layout_survey.add_widget(self.answer_input[-1])
        self.layout_survey.add_widget(self.submit_button)
        self.layout_survey.add_widget(self.result_label)
        self.layout_survey.add_widget(self.close_survey)
        print(self.answer_input[-2].text)
        if self.validate_answer(answer):
            self.current_question_index += 1
            self.answers.append(answer)
            if self.current_question_index < len(self.questions):
                self.update_question()
            else:
                self.check_depression()
            self.answer_input[-1].text = ""
        else:
            self.question_label.text = "Invalid input. Please enter a valid value."

    def validate_answer(self, answer):
        if self.questions[self.current_question_index]["input_type"] == "numeric":
            try:
                numeric_answer = float(answer)
                return self.questions[self.current_question_index]["range"][0] <= numeric_answer <= \
                    self.questions[self.current_question_index]["range"][1]
            except ValueError:
                return False
        elif self.questions[self.current_question_index]["input_type"] == "yes_no":
            return answer.lower().strip() in ["yes", "no"]
        else:
            return False

    def check_depression(self):
        # Criteria for potential depression (modify as needed)
        sleep_hours = float(self.answers[0])
        mood_swings = self.answers[1].lower()
        self_harm_thoughts = self.answers[2].lower()
        meals_per_day = float(self.answers[3])

        if sleep_hours < 6 or mood_swings == "yes" or self_harm_thoughts == "yes" or meals_per_day < 3:
            result = "Based on your answers, you may be showing signs of depression. Please consult a professional."
        else:
            result = "Based on your answers, there are no clear signs of depression. Keep monitoring your well-being."

        self.result_label.text = result

    def close_survey_popup(self, widget):
        self.survey_popup.dismiss()
    def update(self):
        self.update_signin_button()
        self.update_buttons()
        self.update_survey_button()

    def init_buttons(self):

        # self.sign_in_button.append(Rectangle(pos=[x, y - r], size=[width, r]))
        # self.sign_in_button.append(Rectangle(pos=[x - r, y], size=[r, height]))
        # self.sign_in_button.append(Rectangle(pos=[x, y + height], size=[width, r]))
        # self.sign_in_button.append(Rectangle(pos=[x + width, y], size=[r, height]))
        # Color(0, 1, 0, 1)
        # self.sign_in_button.append(Ellipse(pos=[x - r, y - r], size=[2 * r, 2 * r]))
        # self.sign_in_button.append(Ellipse(pos=[x + width - r, y - r], size=[2 * r, 2 * r]))
        # self.sign_in_button.append(Ellipse(pos=[x - r, y + height - r], size=[2 * r, 2 * r]))
        # self.sign_in_button.append(Ellipse(pos=[x + width - r, y + height - r], size=[2 * r, 2 * r]))

        width = int(self.s_width*0.5/2)
        height = int(self.s_height*0.5/2)
        r = int(width / 8)
        x = int(self.s_width*0.2)
        y = int(self.s_height*0.2)
        Color(0.7,0.2,0.8,1)
        self.round_corners3.append(Rectangle(pos = [x,y-r],size=[width, r]))
        self.round_corners3.append(Rectangle(pos = [x-r,y],size=[r, height]))
        self.round_corners3.append(Rectangle(pos = [x,y+height],size=[width, r]))
        self.round_corners3.append(Rectangle(pos = [x+width,y],size=[r, height]))

        self.round_corners3.append(Ellipse(pos = [x-r,y-r],size=[2*r, 2*r]))
        self.round_corners3.append(Ellipse(pos = [x + width - r, y - r],size=[2*r, 2*r]))
        self.round_corners3.append(Ellipse(pos = [x - r, y + height - r],size=[2*r, 2*r]))
        self.round_corners3.append(Ellipse(pos = [x + width - r, y + height - r],size=[2*r, 2*r]))

        x = int(self.s_width * 0.5) + int(self.s_width * 0.1)
        y = int(self.s_height*0.2)
        Color(0.61,0.42,0.11,1)
        self.round_corners4.append(Rectangle(pos=[x, y - r], size=[width, r]))
        self.round_corners4.append(Rectangle(pos=[x - r, y], size=[r, height]))
        self.round_corners4.append(Rectangle(pos=[x, y + height], size=[width, r]))
        self.round_corners4.append(Rectangle(pos=[x + width, y], size=[r, height]))

        self.round_corners4.append(Ellipse(pos=[x - r, y - r], size=[2 * r, 2 * r]))
        self.round_corners4.append(Ellipse(pos=[x + width - r, y - r], size=[2 * r, 2 * r]))
        self.round_corners4.append(Ellipse(pos=[x - r, y + height - r], size=[2 * r, 2 * r]))
        self.round_corners4.append(Ellipse(pos=[x + width - r, y + height - r], size=[2 * r, 2 * r]))

        x = int(self.s_width * 0.2)
        y = int(self.s_height * 0.5) + int(self.s_height*0.05)
        Color(1, 0.35, 0, 1)
        self.round_corners1.append(Rectangle(pos=[x, y - r], size=[width, r]))
        self.round_corners1.append(Rectangle(pos=[x - r, y], size=[r, height]))
        self.round_corners1.append(Rectangle(pos=[x, y + height], size=[width, r]))
        self.round_corners1.append(Rectangle(pos=[x + width, y], size=[r, height]))

        self.round_corners1.append(Ellipse(pos=[x - r, y - r], size=[2 * r, 2 * r]))
        self.round_corners1.append(Ellipse(pos=[x + width - r, y - r], size=[2 * r, 2 * r]))
        self.round_corners1.append(Ellipse(pos=[x - r, y + height - r], size=[2 * r, 2 * r]))
        self.round_corners1.append(Ellipse(pos=[x + width - r, y + height - r], size=[2 * r, 2 * r]))

        x = int(self.s_width * 0.5) + int(self.s_width * 0.05)
        y = int(self.s_height * 0.5) + int(self.s_height * 0.05)
        Color(0,0.7,0.7,1)
        self.round_corners2.append(Rectangle(pos=[x, y - r], size=[width, r]))
        self.round_corners2.append(Rectangle(pos=[x - r, y], size=[r, height]))
        self.round_corners2.append(Rectangle(pos=[x, y + height], size=[width, r]))
        self.round_corners2.append(Rectangle(pos=[x + width, y], size=[r, height]))

        self.round_corners2.append(Ellipse(pos=[x - r, y - r], size=[2 * r, 2 * r]))
        self.round_corners2.append(Ellipse(pos=[x + width - r, y - r], size=[2 * r, 2 * r]))
        self.round_corners2.append(Ellipse(pos=[x - r, y + height - r], size=[2 * r, 2 * r]))
        self.round_corners2.append(Ellipse(pos=[x + width - r, y + height - r], size=[2 * r, 2 * r]))
        self.layout = GridLayout(cols=2)
        self.layout.size = [int(self.s_width*0.6), int(self.s_height*0.6)]
        self.layout.pos_hint={"center_x": 0.5, "center_y": 0.5}
        # 1st row
        self.buttons.append(Button(text='Detect Emotion', background_color = [1,0.35,0,1], background_normal = '', disabled = True))
        self.layout.add_widget(self.buttons[-1])
        self.buttons.append(Button(text='Click To Feel Better!', background_color = [0,0.7,0.7,1], background_normal = '', disabled = True))
        self.layout.add_widget(self.buttons[-1])
        # 2nd row
        self.buttons.append(Button(text='Chat Room', background_color = [0.7,0.2,0.8,1], background_normal = '', disabled = True))
        self.layout.add_widget(self.buttons[-1])
        self.buttons.append(Button(text='Emotion History', background_color = [0.61,0.42,0.11,1], background_normal = '', disabled = True))
        self.layout.add_widget(self.buttons[-1])

        self.add_widget(self.layout)

        self.buttons[0].bind(on_press = self.click1)
        self.buttons[1].bind(on_press = self.click2)
        self.buttons[2].bind(on_press = self.click3)
        self.buttons[3].bind(on_press = self.click4)

    def update_buttons(self):
        width = int(self.s_width * 0.5 / 2)
        height = int(self.s_height * 0.5/2)
        r = int(width / 15)
        x = int(self.s_width * 0.2)
        y = int(self.s_height * 0.2)
        self.round_corners3[0].pos = [x, y - r]
        self.round_corners3[0].size = [width, r]
        self.round_corners3[1].pos = [x - r, y]
        self.round_corners3[1].size = [r, height]
        self.round_corners3[2].pos = [x, y + height]
        self.round_corners3[2].size = [width, r]
        self.round_corners3[3].pos = [x + width, y]
        self.round_corners3[3].size = [r, height]
        self.round_corners3[4].pos=[x - r, y - r]
        self.round_corners3[4].size=[2 * r, 2 * r]
        self.round_corners3[5].pos=[x + width - r, y - r]
        self.round_corners3[5].size=[2 * r, 2 * r]
        self.round_corners3[6].pos=[x - r, y + height - r]
        self.round_corners3[6].size=[2 * r, 2 * r]
        self.round_corners3[7].pos=[x + width - r, y + height - r]
        self.round_corners3[7].size=[2 * r, 2 * r]
        x = int(self.s_width * 0.5) + int(self.s_width * 0.05)
        y = int(self.s_height * 0.2)
        self.round_corners4[0].pos = [x, y - r]
        self.round_corners4[0].size = [width, r]
        self.round_corners4[1].pos = [x - r, y]
        self.round_corners4[1].size = [r, height]
        self.round_corners4[2].pos = [x, y + height]
        self.round_corners4[2].size = [width, r]
        self.round_corners4[3].pos = [x + width, y]
        self.round_corners4[3].size = [r, height]
        self.round_corners4[4].pos = [x - r, y - r]
        self.round_corners4[4].size = [2 * r, 2 * r]
        self.round_corners4[5].pos = [x + width - r, y - r]
        self.round_corners4[5].size = [2 * r, 2 * r]
        self.round_corners4[6].pos = [x - r, y + height - r]
        self.round_corners4[6].size = [2 * r, 2 * r]
        self.round_corners4[7].pos = [x + width - r, y + height - r]
        self.round_corners4[7].size = [2 * r, 2 * r]

        x = int(self.s_width * 0.2)
        y = int(self.s_height * 0.5) + int(self.s_height*0.05)
        self.round_corners1[0].pos = [x, y - r]
        self.round_corners1[0].size = [width, r]
        self.round_corners1[1].pos = [x - r, y]
        self.round_corners1[1].size = [r, height]
        self.round_corners1[2].pos = [x, y + height]
        self.round_corners1[2].size = [width, r]
        self.round_corners1[3].pos = [x + width, y]
        self.round_corners1[3].size = [r, height]
        self.round_corners1[4].pos = [x - r, y - r]
        self.round_corners1[4].size = [2 * r, 2 * r]
        self.round_corners1[5].pos = [x + width - r, y - r]
        self.round_corners1[5].size = [2 * r, 2 * r]
        self.round_corners1[6].pos = [x - r, y + height - r]
        self.round_corners1[6].size = [2 * r, 2 * r]
        self.round_corners1[7].pos = [x + width - r, y + height - r]
        self.round_corners1[7].size = [2 * r, 2 * r]

        x = int(self.s_width * 0.5) + int(self.s_width * 0.05)
        y = int(self.s_height * 0.5) + int(self.s_height * 0.05)
        self.round_corners2[0].pos = [x, y - r]
        self.round_corners2[0].size = [width, r]
        self.round_corners2[1].pos = [x - r, y]
        self.round_corners2[1].size = [r, height]
        self.round_corners2[2].pos = [x, y + height]
        self.round_corners2[2].size = [width, r]
        self.round_corners2[3].pos = [x + width, y]
        self.round_corners2[3].size = [r, height]
        self.round_corners2[4].pos = [x - r, y - r]
        self.round_corners2[4].size = [2 * r, 2 * r]
        self.round_corners2[5].pos = [x + width - r, y - r]
        self.round_corners2[5].size = [2 * r, 2 * r]
        self.round_corners2[6].pos = [x - r, y + height - r]
        self.round_corners2[6].size = [2 * r, 2 * r]
        self.round_corners2[7].pos = [x + width - r, y + height - r]
        self.round_corners2[7].size = [2 * r, 2 * r]

        self.layout.size = [int(self.s_width*0.6), int(self.s_height*0.6)]
        self.layout.spacing = [int(self.s_width*0.1), int(self.s_height*0.1)]
        self.layout.pos = [int(0.2*self.s_width), int(0.2*self.s_height)]

    def click1(self, widget):
        #print("hello world 1")
        self.open_file_manager()

    def open_file_manager(self):
        self.file_manager_obj.show('C:/')
    def exit_manager(self):
        self.file_manager_obj.close()
    def select_path(self, path):
        path = path.replace("\\", "/")
        print(path)
        self.path = path
        if path.endswith("/"):
            layout = GridLayout(cols=1)
            #self.bt2 = Button(text="close", on_release=self.close_err_popup2)
            #layout.add_widget(self.bt2)
            self.err_popup2 = Popup(title="No file was selected",
                                    content=layout,
                                    size_hint=(0.4, 0.2),pos_hint={"center_x": 0.5, "center_y": 0.5}, auto_dismiss=True)
            self.err_popup2.open()
            self.exit_manager()
        elif path.endswith('jpg') or path.endswith('jpeg'):
            print("inside correct if statement")
            self.exit_manager()
            print("manager exited")
            self.perform_action()
        else:
            layout = GridLayout(cols=1)
            #self.bt1 = Button(text="close", on_release=self.close_err_popup1)
            #layout.add_widget(self.bt1)
            self.err_popup1 = Popup(title="Invalid file type\nFile must be jpeg or jpg",content = layout,  size_hint=(0.4, 0.2),pos_hint={"center_x": 0.5, "center_y": 0.5}, auto_dismiss=True)
            self.err_popup1.open()
            self.exit_manager()

    def perform_action(self):
        print("inside perform action")
        label = self.detect_emotion()
        if label:
            emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
            # emoji list
            # print("😊")
            d = {'Happy':"😊", 'Sad':"🥺", 'Fear':"😬😱", 'Neutral':"🫠", 'Disgust':"😖💩", 'Surprise':"😲", 'Angry':"😡"}
            layout = GridLayout(cols=1)
            self.bt2 = Button(text="close", on_release=self.close_emotion_popup)
            layout.add_widget(Label(text=label))
            layout.add_widget(self.bt2)
            self.emotion_popup = Popup(title="RESULTS:",
                                    content=layout,
                                    size_hint=(0.4, 0.25), pos_hint={"center_x": 0.5, "center_y": 0.5},
                                    auto_dismiss=False)
            self.emotion_popup.open()
        else:
            layout = GridLayout(cols=1)
            self.bt2 = Button(text="close", on_release=self.close_emotion_popup)
            layout.add_widget(Label(text="unable to detect emotion"))
            layout.add_widget(self.bt2)
            self.emotion_popup = Popup(title="RESULTS:",
                                       content=layout,
                                       size_hint=(0.4, 0.25), pos_hint={"center_x": 0.5, "center_y": 0.5},
                                       auto_dismiss=False)
            self.emotion_popup.open()
        # //////////////////

        # send()
    def close_emotion_popup(self, widget):
        self.emotion_popup.dismiss()
    def detect_emotion(self):

        # Load pre-trained model
        classifier = load_model("C:/Users/Siddharth Vijayaragh/OneDrive/Desktop/model (1).h5")

        # Load Haar Cascade for face detection
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Emotion labels
        emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

        # Input image path from the user
        #image_path = input("Enter the path to the image file: ")
        image_path = self.path
        # Read the image
        frame = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                label = emotion_labels[prediction.argmax()]
                # label_position = (x, y - 10)
                # cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                label = None

        # cv2_imshow(frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows(
        return label
    def click2(self, widget):
        print("hello world 2")
        l = ["https://youtube.com/shorts/8sYMjLAVcyA?si=CwdL7KJDazSkWt8_", "https://youtube.com/shorts/GNsiCk3grQ0?si=CjgRAysA9mw3zh-v", "https://youtube.com/shorts/8sYMjLAVcyA?si=CwdL7KJDazSkWt8_", "https://youtube.com/shorts/GNsiCk3grQ0?si=CjgRAysA9mw3zh-v", "https://youtube.com/shorts/jj2IDl9Vk6A?si=1qJZSzhZoWGU1lxl"]
        if len(l)!=0:
            s = random.choice(l)
            l.remove(s)
            layout = GridLayout(cols=1)
            layout.add_widget(TextInput(text=s, readonly=True))
            self.feel_better_popup = Popup(title="I bet this video would make your day!",content=layout, size_hint=(0.6, 0.3),pos_hint={"center_x": 0.5, "center_y": 0.5}, auto_dismiss=True)
            self.feel_better_popup.open()

    def click3(self, widget):
        client.close()
        self.layout_chat = GridLayout(cols=1)
        self.close_chat = Button(text="close", size_hint = (1, 0.15), on_press = self.close_chat_popup)
        self.chat_window_instance = BoxLayoutForCHAT((int(self.s_width*0.8), int(self.s_height*0.85)))
        self.layout_chat.add_widget(self.chat_window_instance)
        self.layout_chat.add_widget(self.close_chat)
        self.chat_popup = Popup(title = "Anonymous chatting room", content = self.layout_chat, size=(self.s_width, self.s_height), auto_dismiss = False)
        self.chat_popup.open()

    def close_err_popup1(self):
        self.err_popup1.dismiss()
    def close_err_popup2(self):
        self.err_popup2.dismiss()
    def close_chat_popup(self,widget):
        temp_client = self.chat_window_instance.get_client()
        temp_client.close()
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = client1
        self.chat_popup.dismiss()

    def click4(self, widget):
        values = [[45, 23, 11, 17, 1, 1, 2]]
        labels = ["happy", "fear", "neutral", "surprised", "angry", "sad", "digust"]
        self.layout_graph = GridLayout(cols=1)
        fig = plt.figure()

        for i in range(len(values)):
            plt.subplot(len(values), 1, i+1)
            plt.bar([labels[j] + "\n= " + str(values[i][j]) + "%" for j in range(len(labels))], values[i],
                    color=["red", "green", "blue", "maroon", "orange", "yellow", "purple"],
                    width=0.4)
            plt.title("week "+str(i+1))
            plt.xlabel("Relative Emotions")
            plt.ylabel("Percentage")
            plt.savefig("temp.png")
            self.layout_graph.add_widget(Image(source = "temp.png"))
        button = Button(text="back", size_hint=(0.2, 0.4), pos_hint={"center_x": 0.2, "center_y": 0.2},
                        on_press=self.close_graph_popup)
        self.layout_graph.add_widget(button)
        self.extra_graph_popup = Popup(title="Here are the overall results for this week:", content=self.layout_graph, size_hint=(None, None), size=(self.s_width, self.s_height),
                                 auto_dismiss=False)
        self.extra_graph_popup.open()


    def close_graph_popup(self, widget):
        self.extra_graph_popup.dismiss()


    @staticmethod
    def update_chat_messages(obj, s):
        obj.chat_window_instance.chat_text.text += s

class SentimentAnalysisApp(MDApp):
    pass

SentimentAnalysisApp().run()

