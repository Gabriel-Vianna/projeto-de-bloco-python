from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os
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

        arquivos = os.listdir(os.getcwd())
        arquivos_info = []
        for arquivo in arquivos:
            arquivo_atual = {
                0 : '',
                1 : '',
                2 : '',
                3 : ''
            }
            arquivo_atual[0] = str(arquivo)
            arquivo_atual[1] = str(convert_bytes(os.path.getsize(arquivo)))
            arquivo_atual[2] = datetime.fromtimestamp(os.path.getctime(arquivo)).strftime('%d/%m/%Y %H:%M:%S')
            arquivo_atual[3] = datetime.fromtimestamp(os.path.getmtime(arquivo)).strftime('%d/%m/%Y %H:%M:%S')
            arquivos_info.append(arquivo_atual)
        
        data = {}
        for i in range(len(arquivos_info)):
            data[f'{i+1}'] = arquivos_info[i]

        column_titles = ['Nome arquivo', 'Tamanho', 'Data criação', 'Data alteração']
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