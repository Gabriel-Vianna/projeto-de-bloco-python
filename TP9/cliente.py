# Importações Kivy
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

# Importações de bibliotecas adicionais
from datetime import datetime
import os
import psutil
import socket
import pickle

# Iniciando conexão com o servidor
HOST = socket.gethostname()
PORT = 8881
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect((HOST, PORT))

conexao = "Conexão estabelecida"

bytes_resp = pickle.dumps(conexao)
socket_cliente.send(bytes_resp)

# Recebendo dados de sistema enviados pelo servidor
data = b""
while True:
    packet = socket_cliente.recv(4096)
    if not packet: break
    data += packet

# Tratando os dados recebidos
data_arr = pickle.loads(data)
arquivos_info = data_arr[4]['arquivos']
processos_info = data_arr[5]['processos']
memoria_info = data_arr[0]['memoria']
cpu_info = data_arr[1]['cpu']
disco_info = data_arr[2]['disco']

#Aumentando o tamanho da lista de items de memória e disco para visualmente 
# ficar com uma tabela do mesmo tamanho que as informações de CPU
for i in range(4):
    memoria_info.append('')
    disco_info.append('')

# Encerrando conexão com servidor
socket_cliente.close()

# Configurações de tela
Builder.load_string('''
<FirstPage>:
    id: main_win
    RecycleView:
        viewclass: 'CustomLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustomLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: (self.size)
            pos: self.pos
<SecondPage>:
    id: main_win
    RecycleView:
        viewclass: 'CustomLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<ThirdPage>:
    id: main_win
    RecycleView:
        viewclass: 'CustomLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
''')

# Classe utilizada para renderizar a primeira tela com informações sobre arquivos do servidor
class FirstPage(BoxLayout):
    def __init__(self, table='', **kwargs):
        super().__init__(**kwargs)

        button = Button(text ='Menu', size_hint =(None, 1),
                    pos =(200, 200))
        self.add_widget(button)
        button.bind(on_press=self.switch)

        data = {}
        for i in range(len(arquivos_info)):
            data[f'{i+1}'] = arquivos_info[i]

        column_titles = ['Nome arquivo', 'Tamanho',
                         'Data criação', 'Data alteração']
        indice = [x for x in data.keys()]
        rows_length = 4
        self.columns = 4

        table_data = []
        for y in column_titles:
            table_data.append({'text': str(y), 'size_hint_y': None,
                               'height': 30, 'bcolor': (.05, .30, .80, 1)})

        for z in indice:
            for y in range(rows_length):
                table_data.append({'text': str(
                    data[z][y]), 'size_hint_y': None, 'height': 20, 'bcolor': (.06, .25, .50, 1)})

        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data

    def switch(self, item):
        myapp.screen_manager.current = 'Menu'

# Classe utilizada para renderizar a segunda tela com informações sobre processos do servidor
class SecondPage(BoxLayout):
    def __init__(self,table='', **kwargs):
        super().__init__(**kwargs)

        button = Button(text ='Menu', size_hint =(None, 1),
                    pos =(200, 200))
        self.add_widget(button)
        button.bind(on_press=self.switch)
        
        data = {}
        for i in range(len(processos_info)):
            data[f'{i+1}'] = processos_info[i]

        column_titles = ['Pid', 'Nome', 'Consumo de memória', 'Consumo de CPU']
        indice = [x for x in data.keys()]
        rows_length = 4
        self.columns = 4

        table_data = []
        for y in column_titles:
            table_data.append({'text':str(y),'size_hint_y':None,'height':30,'bcolor':(.05,.30,.80,1)}) 

        for z in indice:
            for y in range(rows_length):
                table_data.append({'text':str(data[z][y]),'size_hint_y':None,'height':20,'bcolor':(.06,.25,.50,1)})

        self.ids.table_floor_layout.cols = self.columns 
        self.ids.table_floor.data = table_data 

    def switch(self, item):
        myapp.screen_manager.current = 'Menu'

# Classe utilizada para renderizar a terceira tela com informações gerais do sistema: Memória, CPU e Disco
class ThirdPage(BoxLayout):
    def __init__(self, table='', **kwargs):
        super().__init__(**kwargs)

        button = Button(text ='Voltar', size_hint =(None, 1),
                    pos =(200, 200))
        self.add_widget(button)
        button.bind(on_press=self.switch)

        infos_gerais = []
        infos_gerais.append(memoria_info)
        infos_gerais.append(cpu_info)
        infos_gerais.append(disco_info)

        data = infos_gerais

        column_titles = ['Informações de memória', 'Informações de CPU', 'Informações de Disco']
        self.columns = 3

        table_data = []
        for y in column_titles:
            table_data.append({'text': str(y), 'size_hint_y': None,
                               'height': 30, 'bcolor': (.05, .30, .80, 1)})

        for z in range(len(infos_gerais[0])):
            for y in range(len(infos_gerais)):
                table_data.append({'text': str(
                    data[y][z]), 'size_hint_y': None, 'height': 20, 'bcolor': (.06, .25, .50, 1)})

        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data
    
    def switch(self, item):
        myapp.screen_manager.current = 'Menu'

# Classe utilizada para renderizar o menu, de onde podemos acessar qualquer tela
class Menu(BoxLayout):
    
    def __init__(self,table='', **kwargs):
        super().__init__(**kwargs)

        """"""
        button = Button(text ='Informações de arquivos', size_hint =(1, .33),
                    pos =(200, 200))
        self.add_widget(button)
        button.bind(on_press=self.switch)

        button = Button(text ='Informações de processos', size_hint =(1, .33),
                    pos =(200, 200))
        self.add_widget(button)
        button.bind(on_press=self.switch)

        button = Button(text ='Informações gerais', size_hint =(1, .33),
                    pos =(200, 200))
        self.add_widget(button)
        button.bind(on_press=self.switch)
        
    def switch(self, item):
        if(item.text == 'Informações de arquivos'):
            myapp.screen_manager.current = 'First'
        elif(item.text == 'Informações de processos'):
            myapp.screen_manager.current = 'Second'
        elif(item.text == 'Informações gerais'):
            myapp.screen_manager.current = 'Third'
        elif(item.text == 'Informações de rede'):
            # myapp.screen_manager.current = 'Fourth'
            pass
            
# Classe que é uma instancia do App e faz o gerenciamento de telas usando o ScreenManager
class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.menu = Menu()
        screen = Screen(name='Menu')
        screen.add_widget(self.menu)
        self.screen_manager.add_widget(screen)

        self.firstPage = FirstPage()
        screen = Screen(name='First')
        screen.add_widget(self.firstPage)
        self.screen_manager.add_widget(screen)

        self.secondPage = SecondPage()
        screen = Screen(name='Second')
        screen.add_widget(self.secondPage)
        self.screen_manager.add_widget(screen)

        self.thirdPage = ThirdPage()
        screen = Screen(name='Third')
        screen.add_widget(self.thirdPage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

myapp = MyApp()
myapp.run()
