# Imports de bibliotecas
import os
import platform
import sched
import subprocess
import time
from datetime import datetime
import psutil
from cpuinfo import cpuinfo
import nmap
import socket
import pickle

# Função que retorna informações sobre memória do servidor
def obter_info_memoria():
    memoria_info = []
    memoria = psutil.virtual_memory()
    memoria_total = round(memoria.total / (1024 * 1024 * 1024), 2)
    memoria_disponivel = round(memoria.available / (1024 * 1024 * 1024), 2)
    memoria_uso = memoria_total - memoria_disponivel
    memoria_porcentagem = round(memoria_uso * 100 / memoria_total, 2)
    memoria_info.append('Total de memória: ' + str(memoria_total))
    memoria_info.append('Memória disponível: ' + str(memoria_disponivel))
    memoria_info.append('Memória em uso: ' + str(memoria_uso))
    memoria_info.append('Porcentagem: ' + str(memoria_porcentagem))
    return memoria_info

# Função que retorna informações sobre a CPU do servidor
def obter_info_cpu():
    cpu_info = []
    cpu = cpuinfo.get_cpu_info()
    cpu_porcentagem_por_nucleo = psutil.cpu_percent(interval=1, percpu=True)
    cpu_info.append('Arquitetura: ' + str(cpu['arch']))
    cpu_info.append('Modelo da CPU: ' + str(cpu['brand_raw']))
    cpu_info.append('Palavra: ' + str(cpu['bits']))
    cpu_info.append('Frequência total: ' + str(cpu['hz_advertised']))
    cpu_info.append('Frequência de uso: ' + str(cpu['hz_actual']))
    cpu_info.append('Número de núcleos lógicos: ' + str(cpu['count']))
    cpu_info.append('Número de núcleos físicos: ' +  str(psutil.cpu_count(logical=False)))
    cpu_info.append('Porcentagem: ' + str(cpu_porcentagem_por_nucleo))
    return cpu_info

# Função que retorna informações sobre Disco do servidor
def obter_info_disco():
    disco_info = []
    disco = psutil.disk_usage('.')
    disco_total = round(disco.total, 2)
    disco_disponivel = round(disco.free, 2)
    disco_uso = round(disco.used, 2)
    disco_percentual_usado = round(disco.percent, 2)
    disco_info.append('Disco total: ' + str(convert_bytes(disco_total)))
    disco_info.append('Disponível em disco: ' + str(convert_bytes(disco_disponivel)))
    disco_info.append('Disco em uso: ' + str(convert_bytes(disco_uso)))
    disco_info.append('Porcentagem: ' + str(convert_bytes(disco_percentual_usado)))
    return disco_info

# Função que retorna informações de redes
def obter_info_redes():
    interfaces = psutil.net_if_addrs()
    nomes = []
    for i in interfaces:
        nomes.append(str(i))
    for i in nomes:
        print(i + ":")
        for j in interfaces[i]:
            print("\t" + str(j))

    return interfaces

def dados_rede_interface():
    info_redes = psutil.net_io_counters(pernic=True)
    redes = []
    nomes = []
    for info in info_redes:
        nomes.append(str(info))
    for nome in nomes:
        rede = {'nome': nome, 'enviado': info_redes[nome][0], 'recebido': info_redes[nome][1]}
        redes.append(rede)
    return redes

print(dados_rede_interface())

def dados_rede_processo():
    processos_rede = psutil.net_io_counters()
    rede = {'bytes_enviados': processos_rede[0], 'bytes_recebidos': processos_rede[1]}
    return rede

print(dados_rede_processo())
    
# Função que retorna os arquivos e suas propriedades do diretório onde o servidor está rodando
def detalhes_pasta():
    arquivos = os.listdir(os.getcwd())
    arquivos_info = []
    for arquivo in arquivos:
        arquivo_atual = {
            0: '',
            1: '',
            2: '',
            3: ''
        }
        arquivo_atual[0] = str(arquivo)
        arquivo_atual[1] = str(convert_bytes(os.path.getsize(arquivo)))
        arquivo_atual[2] = datetime.fromtimestamp(
            os.path.getctime(arquivo)).strftime('%d/%m/%Y %H:%M:%S')
        arquivo_atual[3] = datetime.fromtimestamp(
            os.path.getmtime(arquivo)).strftime('%d/%m/%Y %H:%M:%S')
        arquivos_info.append(arquivo_atual)

    return arquivos_info

# Função que retorna a lista com todos os processos ativos e suas propriedades
def obter_pids():
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
        if psutil.pid_exists(processo.info['pid']):
            processo_atual[2] = convert_bytes(psutil.Process(processo.info['pid']).memory_info()[0])
            processo_atual[3] = psutil.Process(processo.info['pid']).cpu_percent()
        else:
            pass
        processos_info.append(processo_atual)

    return processos_info

# Printa todos os Pids de processos
def print_pids():
    # print(obter_pids())
    pass

# Printa todos os arquivos das pastas
def print_pasta():
    # print(detalhes_pasta())
    pass

# Função que mede a duração da função de escalonamento
def escalonar_funcoes():
    scheduler = sched.scheduler(time.time, time.sleep)
    inicio = time.time()
    scheduler.enter(1, 1, print_pids)
    scheduler.enter(2, 1, print_pasta)
    scheduler.run()
    fim = time.time()
    duracao = fim - inicio
    return f'Duração da função escalonada em segundos: {duracao}.'

# Função que retorna as interfaces de rede disponíveis no servidor
def obter_interfaces():
    interfaces = psutil.net_if_addrs()
    nomes = []
    redes = []
    for i in interfaces:
        nomes.append(str(i))
    for nome in nomes:
        for j in interfaces[nome]:
            rede = {'family': j[0], 'endereco': j[2], 'mascara': j[3]}
            redes.append(rede)

    return redes


obter_interfaces()

# Função que valida se um IP é válido
def ip_valido(ip):
    # eh valido se for da classe c
    strings = ip.split('.')
    numeros = [int(string) for string in strings]

    if (192 <= numeros[0] <= 223) and (0 <= numeros[-3] <= 255):
        return True
    else:
        return False

def retornar_ip_valido():
    ip_string = input("Entre com o IP alvo: ")
    while not ip_valido(ip_string):
        ip_string = input("IP inválido. Entre com o IP alvo: ")
    if ip_valido(ip_string):
        return ip_string

def retorna_codigo_ping(hostname):
    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]
    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]
    ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    return ret_cod


def verifica_hosts(base_ip):
    host_validos = []
    return_codes = dict()
    for i in range(1, 255):
        return_codes[base_ip + '{0}'.format(i)] = retorna_codigo_ping(base_ip + '{0}'.format(i))
        if i % 20 == 0:
            print(".", end="")
        if return_codes[base_ip + '{0}'.format(i)] == 0:
            host_validos.append(base_ip + '{0}'.format(i))
    print("Hosts válidos: ", host_validos)
    return host_validos

def informacoes_portas(base_ip):
    host = verifica_hosts(base_ip)[0]
    nm = nmap.PortScanner()
    nm.scan(host)
    portas = []
    for proto in nm[host].all_protocols():
        print('----------')
        print('Protocolo : %s' % proto)
        lport = nm[host][proto].keys()
        for port in lport:
            portas.append('Porta: %s\t Estado: %s' % (port, nm[host][proto][port]['state']))
    return portas


def obter_hostnames(host_validos):
    nm = nmap.PortScanner()
    hostnames = []
    for i in host_validos:
        try:
            nm.scan(i)
            print(f'O IP {i} possui o nome {nm[i].hostname()}')
            hostnames.append(nm[i].hostname())
        except:
            pass
    return hostnames

# Função que faz a conversão entre as grandezas dos tamanhos de arquivos
def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

    return size

# Abrindo uma conexão e esperando conectividade com o cliente
HOST = socket.gethostname()
PORT = 8881
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((HOST, PORT))
socket_servidor.listen()
print("Esperando conexão")
(socket_cliente, endereco) = socket_servidor.accept()
print("Conectado a: ", str(endereco))


obter_info_redes()
ip_string = retornar_ip_valido()
ip_lista = ip_string.split('.')
base_ip = ".".join(ip_lista[0:3])
rede = ".".join(ip_lista[0:3]) + '.'
print("O teste será feito na sub rede: ", base_ip)

memoria = obter_info_memoria()
cpu = obter_info_cpu()
disco = obter_info_disco()
redes = obter_info_redes()
arquivos = detalhes_pasta()
processos = obter_pids()
tempo_escalonamento = escalonar_funcoes()
# portas = informacoes_portas(base_ip)

# Reunindo informações sobre o servidor para enviar ao cliente
informacoes = [{'memoria': memoria}, {'cpu': cpu}, {'disco': disco}, {'redes': redes}, {'arquivos': arquivos},
               {'processos': processos}, {'tempo_escalonamento': tempo_escalonamento}]

# Envio das informações
socket_cliente.send(pickle.dumps(informacoes))
bytes = socket_cliente.recv(1024)
lista = pickle.loads(bytes)

# Fechando conexão
socket_servidor.close()