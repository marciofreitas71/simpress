from datetime import datetime, timedelta
import repository_gestao_impressoras as repo

def salva_dados_csv():
    DateTimeEnd = datetime.strptime('2024-04-25', '%Y-%m-%d')

    # Quantidade de dias anteriores à data final
    dias = 1

    while dias < 800:
        # Recupera dados do webservice
        dados_webservice = repo.recuperar_dados_webservice(DateTimeEnd.strftime('%Y-%m-%d'))
        
        # Adiciona a nova coluna com a DateTimeEnd
        dados_webservice['RealDataCapture'] = DateTimeEnd.strftime('%Y-%m-%d')
        
        # Salva os dados em um arquivo CSV
        dados_webservice.to_csv(f'arquivos/dados-{DateTimeEnd.strftime("%Y-%m-%d")}.csv', index=False)
        
        print(f'Dados do dia {DateTimeEnd.strftime("%Y-%m-%d")} processados e salvos')
        
        dias += 1       
        # Atualiza a data para o dia anterior
        DateTimeEnd -= timedelta(days=1)

salva_dados_csv()
