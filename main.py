import os
import logging
import time
from utils import utils
from app import crud
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from threading import Thread

def insere_webservice_bd():
    """
    Insere dados do webservice no banco de dados.

    Chama a função insere_websersvice_banco do módulo utils e faz o logging das
    etapas de execução e conclusão.
    """
    logging.info("Executando insere_websersvice_banco")
    utils.insere_webservice_banco()
    logging.info("Execução de insere_websersvice_banco concluída")

def verificar_condicao_de_espera():
    """
    Loop contínuo para verificar e logar a condição de espera a cada minuto.

    Esta função imprime os jobs agendados pelo scheduler e loga a hora atual
    a cada minuto. Permanece em execução até que uma interrupção (Ctrl+C) seja recebida.
    """
    while True:
        now = datetime.now()
        logging.info(f'Aguardando execução. Hora atual: {now.strftime("%Y-%m-%d %H:%M:%S")}')
        scheduler.print_jobs()  # Imprime os jobs agendados
        print('Aguardando execução. Pressione Ctrl+C para interromper.')
        time.sleep(60)  # Verifica a cada minuto

if __name__ == "__main__":
    # Cria a pasta logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configuração do logging
    logging.basicConfig(filename='logs/scheduler.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Scheduler iniciado')

    # Configuração do agendamento
    scheduler = BlockingScheduler()

    # Adiciona um trabalho ao scheduler para executar insere_webservice_bd diariamente às 02:00:00
    scheduler.add_job(insere_webservice_bd, 'cron', hour=2, minute=0, second=0)

    try:
        logging.info('Scheduler em execução')

        # Inicia o scheduler em um thread separado para permitir o loop de verificação
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()

        # Inicia a verificação da condição de espera
        verificar_condicao_de_espera()

    except (KeyboardInterrupt, SystemExit):
        logging.info('Scheduler interrompido')
        # Encerra o scheduler de forma segura
        scheduler.shutdown()
