import os
import time

# Como é opcional o uso do pygame, o sistema exibirá os resultados no terminal


#Exibe informações sobre os arquivos presentes na pasta atual

# Obtém lista de arquivos e diretórios do diretório corrente:
lista = os.listdir()
dic = {} # cria dicionário
for i in lista: # Varia na lista dos arquivos e diretórios
    if os.path.isfile(i): # checa se é um arquivo
# Cria uma lista para cada arquivo. Esta lista contém o
# tamanho, data de criação e data de modificação.
        dic[i] = []
        dic[i].append(os.stat(i).st_size) # Tamanho
        dic[i].append(os.stat(i).st_atime) # Tempo de criação
        dic[i].append(os.stat(i).st_mtime) # Tempo de modificação

titulo = '{:11}'.format("Tamanho")  # 10 caracteres + 1 de espaço

# Concatenar com 25 caracteres + 2 de espaços
titulo = titulo + '{:27}'.format("Data de Modificação")

# Concatenar com 25 caracteres + 2 de espaços
titulo = titulo + '{:27}'.format("Data de Criação")

titulo = titulo + "Nome"
print(titulo)

for i in dic:
    kb = (dic[i][0])/1000
    tamanho = '{:10}'.format(str('{:.2f}'.format(kb)) + ' KB')
    print(tamanho, time.ctime(dic[i][2])," ", time.ctime(dic[i][1]), " ", i)




# Separa os arquivos dos diretórios presentes na pasta e lista eles separadamente
import os
lista = os.listdir()
lista_arq = [] # lista para guardar os arquivos
lista_dir = [] # lista para guardar os diretórios
for i in lista:
    if os.path.isfile(i):
        lista_arq.append(i)
    else:
        lista_dir.append(i)

# Checa se tem arquivo na lista
if len(lista_arq) > 0:
    print("Arquivos:")
    for i in lista_arq:
        print("\t"+i) # insere uma tabulação no início
    print("") # Quebra de linha

# Checa se tem diretório na lista
if len(lista_dir) > 0:
    print("Diretórios:")
    for i in lista_dir:
        print("\t"+i) # insere uma tabulação no início
    print("") # Quebra de linha



# Exibe os arquivos de acordo com sua extensão
import os

lista = os.listdir()
dic_arq = {} # Usar dicionário para guardar os arquivos por tipo
for i in lista:
    if os.path.isfile(i):
        ext = os.path.splitext(i)[1] # Separa em nome e extensão
        # Verifica se a extensão está presente no dicionário:
        if not ext in dic_arq:
            dic_arq[ext] = []
            dic_arq[ext].append(i) # Usa a extensão como chave
print(dic_arq)



# Lista os arquivos e diretórios presentes 

for i in dic_arq: 
    print("Arquivos " + i)
    for j in dic_arq[i]:
        print("\t"+j)
    print("")
if len(lista_dir) > 0:
    print("Diretórios:")
    for i in lista_dir:
        print("\t"+i)
    print("")



#Recebe um diretório do usuário e lista seus arquivos informando seu tamanho
import os
p_dir = input("Entre com o diretório: ")
if os.path.isdir(p_dir):
    somador = 0
    lista = os.listdir(p_dir)
    for i in lista:
        p = os.path.join(p_dir, i)
        if os.path.isfile(p):
            somador = somador + os.stat(p).st_size

        print("Tamanho:", somador/1000, "KB")
else:
    print("O diretório", '\''+p_dir+'\'', "não existe.")


# Recebe um diretório do usuário e retorna o tamanho do seu maior arquivo
import os

lista_dir = []
entrada = input("Entre com o diretório: ")

if os.path.isdir(entrada):
    lista_dir.append(entrada)
    somador = 0
    p_dir = ""
    while lista_dir:
        diretorio = lista_dir[0]
        p_dir = os.path.join(p_dir, diretorio)
        lista = os.listdir(p_dir)
        for i in lista:
            p = os.path.join(p_dir, i)
            if os.path.isdir(p):
                lista_dir.append(i)
            elif os.path.isfile(p):
                somador = somador + os.stat(p).st_size
        lista_dir.remove(diretorio)
    print(str(somador/1000) + " KB")
else:
    print("O diretório", '\''+p_dir+'\'', "não existe.")



# Recebe um nome de processo do usuário e exibe seu PID, ou informa se o processo não está em execução

import psutil
nome = input("Entre com o nome do processo a ser buscado: ")
lp = psutil.pids()
lista_pid = []
for i in lp:
    p = psutil.Process(i)
    if p.name() == nome:
        lista_pid.append(str(i))

if len(lista_pid) > 0:
    print("O(s) PID(s) de", nome, "são:")
    print(', '.join(lista_pid))
else:
    print(nome, "não está executando no momento.")


# Pega um processo em execução do sistema e exibe suas informações

import subprocess, psutil, time
# Apenas cria um processo (calculadora) para testar
# pid = subprocess.Popen("calc").pid
pid = psutil.pids()[0]
p = psutil.Process(pid)
print("Nome:", p.name())
print("Executável:", p.exe())
print("Tempo de criação:", time.ctime(p.create_time()))
print("Tempo de usuário:", p.cpu_times().user, "s")
print("Tempo de sistema:", p.cpu_times().system, "s")
print("Percentual de uso de CPU:", p.cpu_percent(interval=1.0), "%")
perc_mem = '{:.2f}'.format(p.memory_percent())
print("Percentual de uso de memória:", perc_mem, "%")
# RSS: Resident set size e VMS: Virtual Memory Size
mem = '{:.2f}'.format(p.memory_info().rss/1024/1024)
print("Uso de memória:", mem, "MB")
print("Número de threads:", p.num_threads())