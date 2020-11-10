from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar

import sqlite3
import requests
import time

Window.size = (400,600)

conn = sqlite3.connect('C:\Olamundo1.db')
cursor = conn.cursor()

class Gerenciador(ScreenManager):
    pass

class Menu(Screen):
    pass

class Calculadora(Screen):
    pass

class Arduino(Screen):
    def __init__(self,temperaturas=[],**kwargs):
        super().__init__(**kwargs)
        for tarefa in temperaturas:
            self.ids.box.add_widget(Temp(text=tarefa))



    def addWidget(self):
        ti = requests.get("https://api.thingspeak.com/channels/1221016/fields/1.json?api_key=L38FF3QI01X9GHSH&results=2")
        resp = ti.json()
        temperatura1 = resp['feeds'][1]['field1']
        data_atualizada = str(resp['feeds'][1]['created_at'])
        hora1 = (int(data_atualizada[11:13]) - 3)
        hora2 = (int(data_atualizada[14:16]) + 1)
        temperatura = ('Temperatura: ' + temperatura1 + '\n ' + 'Data Registrada - ' + str(hora1) + ':' + str(
            hora2) + ' - ' + data_atualizada[8:10] + '/' + data_atualizada[5:7] + '/' + data_atualizada[0:4])
        date = (data_atualizada[8:10] + '/' + data_atualizada[5:7] + '/' + data_atualizada[0:4] + ' - ' + str(hora1) + ':' + str(hora2))

        self.ids.box.add_widget(Temp(text=temperatura))

        cursor.execute("insert into Temperatura (temperatura,data_ocorrencia) values (" + temperatura1 + ",'" + date + "')")
        conn.commit()



class Temp(BoxLayout):
    def  __init__(self,text='',**kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = text


class appApp(MDApp):
    def build(self):
        self.icon = 'una2.png'
        return Gerenciador()


appApp().run()


