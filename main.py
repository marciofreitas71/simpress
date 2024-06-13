import os
import logging
import time
from utils import utils
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from threading import Thread

# Função que será agendada para execução
def insere_webservice_bd():
    """
    Chama a função insere_websersvice_banco do módulo utils e faz o logging.
    
    Esta função é responsável por inserir dados do webservice no banco de dados.
    A execução e a conclusão da função são registradas no log.
    """
    logging.info("Executando insere_websersvice_banco")
    utils.insere_webservice_banco()
    logging.info("Execução de insere_websersvice_banco concluída")

# def verificar_condicao_de_espera():
#     while True:
#         now = datetime.now()
#         logging.info(f'Aguardando execução. Hora atual: {now.strftime("%Y-%m-%d %H:%M:%S")}')
#         scheduler.print_jobs()  # Imprime os jobs agendados
#         print('Aguardando execução. Pressione Ctrl+C para interromper.')

#         time.sleep(60)  # Verifica a cada minuto

if __name__ == "__main__":
    # # Cria a pasta logs se não existir
    # if not os.path.exists('logs'):
    #     os.makedirs('logs')

    # # Configuração do logging
    # logging.basicConfig(filename='logs/scheduler.log', level=logging.INFO,
    #                     format='%(asctime)s - %(levelname)s - %(message)s')
    # logging.info('Scheduler iniciado')

    # # Configuração do agendamento
    # scheduler = BlockingScheduler()

    # # Adiciona um trabalho ao scheduler para executar insere_webservice_bd diariamente às 16:56:00
    # scheduler.add_job(insere_webservice_bd, 'cron', hour=2, minute=00, second=0)

    # try:
    #     logging.info('Scheduler em execução')

    #     # Inicia o scheduler em um thread separado para permitir o loop de verificação
    #     scheduler_thread = Thread(target=scheduler.start)
    #     scheduler_thread.start()

    #     # Inicia a verificação da condição de espera
    #     verificar_condicao_de_espera()

    # except (KeyboardInterrupt, SystemExit):
    #     logging.info('Scheduler interrompido')
    #     # Encerra o scheduler de forma segura
    #     scheduler.shutdown()
    insere_webservice_bd()