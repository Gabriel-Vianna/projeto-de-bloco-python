from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os
import psutil
from datetime import datetime

#kv codes
Builder.load_string('''
<DataTable>:
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
            size: self.size
            pos: self.pos
''')

def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

    return size

class DataTable(BoxLayout):
    def __init__(self,table='', **kwargs):
        super().__init__(**kwargs)

        processos = psutil.process_iter(['pid', 'name', 'username'])
        processos = list(processos)
        processos_info = []
        for processo in processos:
            processo_atual = {
                0 : '',
                1 : '',
                2 : '',
                3 : ''
            }
            processo_atual[0] = processo.info['pid']
            processo_atual[1] = processo.info['name']
            processo_atual[2] = convert_bytes(psutil.Process(processo.info['pid']).memory_info()[0])
            processo_atual[3] = psutil.Process(processo.info['pid']).cpu_percent()
            processos_info.append(processo_atual)
        
        data = {}
        for i in range(len(processos_info)):
            data[f'{i+1}'] = processos_info[i]

        column_titles = ['Pid', 'Nome', 'Consumo de memória', 'Consumo de CPU']
        indice = [x for x in data.keys()]
        rows_length = 4
        self.columns = 4

        table_data = []
        for y in column_titles:
            table_data.append({'text':str(y),'size_hint_y':None,'height':30,'bcolor':(.05,.30,.80,1)}) #append the data

        for z in indice:
            for y in range(rows_length):
                table_data.append({'text':str(data[z][y]),'size_hint_y':None,'height':20,'bcolor':(.06,.25,.50,1)}) #append the data

        self.ids.table_floor_layout.cols = self.columns #define value of cols to the value of self.columns
        self.ids.table_floor.data = table_data #add table_data to data value

class DataTableApp(App):
    def build(self):
        return DataTable()

if __name__=='__main__':
    DataTableApp().run()