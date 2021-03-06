from datetime import datetime
import os
import subprocess
import platform
import pygame
import psutil
import cpuinfo
import sched
import time
import nmap

pygame.init()
pygame.font.init()
font = pygame.font.Font("roboto.ttf", 22)
pygame.display.set_caption("Ana Paula - TP4")
bege = (245, 245, 220)
cinza = (170, 170, 170)
azul = (0, 128, 214)
preto = (0, 0, 0)
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
tela.fill(preto)


def retorna_codigo_ping(hostname):
    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]

    ret_cod = subprocess.call(args,
                              stdout=open(os.devnull, 'w'),
                              stderr=open(os.devnull, 'w'))
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
    print("\nMapping ready...")

    return host_validos


hosts_validos = verifica_hosts("172.217.28.100")


def obter_hostnames(host_validos):
    nm = nmap.PortScanner()
    for i in host_validos:
        try:
            nm.scan(i)
        except:
            pass


ip_string = input("Entre com o ip alvo: ")
ip_lista = ip_string.split('.')
base_ip = ".".join(ip_lista[0:3]) + '.'


def desenhar_barra(porcentagem):
    largura_barra = 600
    altura_barra = 40

    pygame.draw.rect(tela, cinza, (((LARGURA_TELA - largura_barra) / 2), 40, largura_barra, altura_barra))
    larg_barra = largura_barra * porcentagem / 100
    pygame.draw.rect(tela, azul, (((LARGURA_TELA - largura_barra) / 2), 40, larg_barra, altura_barra))


def criar_tela(obj):
    tela.fill(bege)
    altura  = 150
    for i in obj:
        texto = font.render(f'{i}: {obj[i]}', 1, preto)
        tela.blit(texto, (20, altura))
        altura += 40
    if 'Porcentagem' in obj:
        desenhar_barra(obj['Porcentagem'])


def detalhes_pasta():
    lista = os.listdir()
    arquivos = []

    for i in lista:
        arquivo = {}
        if os.path.isfile(i):
            nome = i
            arquivo['Nome'] = nome
            tamanho_mb = os.stat(i).st_size / 1000
            arquivo['Tamanho'] = f'{tamanho_mb}kb'
            criacao = datetime.fromtimestamp(os.stat(i).st_atime).strftime('%d/%m/%Y')
            arquivo['Cria????o'] = criacao
            modificacao = datetime.fromtimestamp(os.stat(i).st_mtime).strftime('%d/%m/%Y')
            arquivo['??ltima modifica????o'] = modificacao
        arquivos.append(arquivo)

    return arquivos

detalhes_pasta()


def obter_pids():
    p = psutil.Process()
    processos = {}
    processos['PIDs'] = psutil.pids()
    p = psutil.Process(processos['PIDs'][-1])
    print(p)
    processos['N??mero de threads'] = p.num_threads()
    processos['Nome do usu??rio'] = p.username()

    return processos


def print_pids():
    pids = obter_pids()
    print(pids)


def print_pasta():
    pasta = detalhes_pasta()
    print(pasta)


def criar_tela_arquivo(arquivos):
    tela.fill(bege)
    altura  = 60
    tela.fill(bege)
    for arquivo in arquivos:
        for item in arquivo:
            texto = font.render(f'{item}: {arquivo[item]}', 1, preto)
            tela.blit(texto, (20, altura))
            altura += 40


scheduler = sched.scheduler(time.time, time.sleep)
inicio = time.time()
scheduler.enter(5, 1, print_pids)
scheduler.enter(3, 1, print_pasta)
scheduler.run()
fim = time.time()
duracao = fim - inicio
print(f'Dura????o em segundos: {duracao}.')

memoria = psutil.virtual_memory()
memoria_total = round(memoria.total/(1024 * 1024 * 1024), 2)
memoria_disponivel = round(memoria.available/(1024 * 1024 * 1024), 2)
memoria_uso = memoria_total - memoria_disponivel
memoria_porcentagem = round(memoria_uso * 100 / memoria_total, 2)
dict_memoria = {'Total de mem??ria': memoria_total, 'Mem??ria dispon??vel': memoria_disponivel, 'Mem??ria em uso': memoria_uso, 'Porcentagem': memoria_porcentagem}

cpu_porcentagem = psutil.cpu_percent()
cpu_plataforma = platform.platform()
cpu = cpuinfo.get_cpu_info()
dict_cpu = {'Arquitetura': cpu['arch'], 'Modelo da CPU': cpu['brand_raw'], 'Palavra': cpu['bits'], 'Frequ??ncia total': cpu['hz_advertised'], 'Frequ??ncia de uso': cpu['hz_actual'], 'N??mero de n??cleos l??gicos': cpu['count'], 'N??mero de n??cleos f??sicos': psutil.cpu_count(logical=False), 'Porcentagem': cpu_porcentagem}

disco = psutil.disk_usage('.')
disco_total = round(disco.total, 2)
disco_disponivel = round(disco.free, 2)
disco_uso = round(disco.used, 2)
disco_percentual_usado = round(disco.percent, 2)
dict_disco = {'Disco total': disco_total, 'Dispon??vel em disco': disco_disponivel, 'Disco em uso': disco_uso, 'Porcentagem': disco_percentual_usado}

interfaces_redes = psutil.net_if_addrs()
endereco_ip = {'Endere??o IP': interfaces_redes['Wi-Fi'][0].address}
crashed = False
posicao = 0

dic_os = detalhes_pasta()
processo = obter_pids()

while not crashed:
    if posicao == 0:
        criar_tela(dict_memoria)
    elif posicao == 1:
        criar_tela(dict_cpu)
    elif posicao == 2:
        criar_tela(dict_disco)
    elif posicao == 3:
        criar_tela(endereco_ip)
    elif posicao == 4:
        criar_tela_arquivo(dic_os)
    elif posicao == 5:
        criar_tela(processo)
    elif posicao == 6:
        criar_tela_arquivo(hosts_validos)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if posicao < 5:
                    posicao += 1
                else:
                    posicao = 0
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if posicao > 0:
                    posicao -= 1
                else:
                    posicao = 6

    pygame.display.update()

pygame.quit()
quit()
