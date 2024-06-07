from app import webservice, crud
from utils import utils
import logging   
from apscheduler.schedulers.blocking import BlockingScheduler
import os

def insere_webservice_bd():
    """
    Chama a função insere_websersvice_banco do módulo utils e faz o logging.
    
    Esta função é responsável por inserir dados do webservice no banco de dados.
    A execução e a conclusão da função são registradas no log.
    """
    logging.info("Executando insere_websersvice_banco")
    utils.insere_webservice_banco()
    logging.info("Execução de insere_websersvice_banco concluída")

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
    # # Adiciona um trabalho ao scheduler para executar insere_websersvice_bd diariamente às 3:00:00
    # scheduler.add_job(insere_websersvice_bd, 'cron', hour=16, minute=56, second=0)

    # try:
    #     logging.info('Scheduler em execução')
    #     # Inicia o scheduler para começar a execução das tarefas agendadas
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     logging.info('Scheduler interrompido')
    #     # Encerra o scheduler de forma segura
    #     scheduler.shutdown()

    insere_webservice_bd()
