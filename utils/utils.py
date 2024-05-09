def insere_dados_csv_to_bd():
    """
    Insere registros do webservice a partir de um arquivo csv.

    Lê um arquivo CSV contendo dados do webservice e insere esses registros em um banco de dados.
    
    Arquivo CSV esperado: 'testes/arquivos_final/arquivo_final-06-04-2024.csv'
    O arquivo deve conter as seguintes colunas:
    - 'RealDateCapture': Data de captura no formato 'YYYY-MM-DD'
    - 'PrinterDeviceID': ID da impressora
    - 'ReferenceMono': Referência de impressões monocromáticas
    - 'ReferenceColor': Referência de impressões coloridas
    
    Cada registro é inserido no banco de dados utilizando a função 'create_contagem_impressoras'
    do módulo 'crud'.

    Se ocorrer algum erro durante a inserção, uma mensagem de erro é impressa, e o programa continua a execução.
    """
        df = pd.read_csv('testes/arquivos_final/arquivo_final-06-04-2024.csv')
        total = len(df)
        contagem = 10024


        # # # print(df.columns)
        for index, row in df.iterrows():
        
            # String com a data
            data_string = row['RealDateCapture']

            # Converter a string em um objeto datetime
            data_datetime = datetime.strptime(data_string, '%Y-%m-%d')


            try:
                # Tentar inserir os dados
                crud.create_contagem_impressoras(row['PrinterDeviceID'], row['ReferenceMono'], row['ReferenceColor'], data_datetime)
                print(f"Registro  ({row['PrinterDeviceID']}) inserido com sucesso.")
            except Exception as e:
                # Capturar qualquer exceção e imprimir uma mensagem de erro
                print(f"Erro ao inserir registro de contagem - impressora {row['PrinterDeviceID']}: {str(e)}")
                print(f'{row['SerialNumber']} - {row['DateTimeRead']}')
            contagem += 1
            print(f'Inseridos {contagem} de {total}')
            os.system('cls')

def inserir_impressoras_from_csv(nome_arquivo):

    # Cria uma instância do mecanismo de conexão
    engine = repo.getConnection()

    # Cria um objeto de sessão
    Session = sessionmaker(bind=engine)
    session = Session()
    # Ler o arquivo CSV para um DataFrame do Pandas
    df = pd.read_csv(nome_arquivo)

    # Iterar sobre as linhas do DataFrame
    for index, linha in df.iterrows():
        # Extrair os valores dos campos do DataFrame
        PRINTERDEVICEID = linha['PrinterDeviceID']
        PRINTERBRANDNAME = linha['BrandName']
        PRINTERMODELNAME = linha['PrinterModelName']
        SERIALNUMBER = linha['SerialNumber']

        CREATED_AT = datetime.now()
        STATUS = 1  # Definir o status como 1

        # Verificar se já existe uma impressora com o mesmo PRINTERDEVICEID
        exists_query = session.query(PRINTERDEVICEID).filter(CONTAGEM_IMPRESSORA.PRINTERDEVICEID == PRINTERDEVICEID).first()
        if exists_query:
            print(f"Impressora com PRINTERDEVICEID {PRINTERDEVICEID} já existe no banco de dados. Ignorando inserção.")
        else:
            # Se não existe, criar a impressora
            repo.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)

def salva_dados_csv(DateTimeEnd,service_method, payload, timeout, wsdl_url):
     """
    Insere impressoras a partir de um arquivo CSV no banco de dados.

    Args:
        nome_arquivo (str): O caminho do arquivo CSV contendo os dados das impressoras.

    Esta função lê um arquivo CSV contendo informações sobre impressoras e as insere no banco de dados.
    O arquivo CSV deve ter as seguintes colunas:
    - 'PrinterDeviceID': ID da impressora
    - 'BrandName': Nome da marca da impressora
    - 'PrinterModelName': Nome do modelo da impressora
    - 'SerialNumber': Número de série da impressora

    As impressoras são inseridas no banco de dados utilizando a função 'create_impressora' do módulo 'repo'.

    Se uma impressora com o mesmo 'PrinterDeviceID' já existe no banco de dados, a inserção é ignorada.

    Exemplo:
    >>> inserir_impressoras_from_csv('caminho/do/arquivo.csv')
    """
    
   # Quantidade de dias anteriores à data final
    dias = 1

    while dias < 800:
        # Recupera dados do webservice
        dados_webservice = repo.recuperar_dados_webservice(wsdl_url, service_method, payload)
        
        # Adiciona a nova coluna com a DateTimeEnd
        dados_webservice['RealDataCapture'] = DateTimeEnd.strftime('%Y-%m-%d')
        
        # Salva os dados em um arquivo CSV
        dados_webservice.to_csv(f'testes/arquivos_final/dados-{DateTimeEnd.strftime("%Y-%m-%d")}.csv', index=False)
        
        print(f'Dados do dia {DateTimeEnd.strftime("%Y-%m-%d")} processados e salvos')
        
        dias += 1       
        # Atualiza a data para o dia anterior
        DateTimeEnd -= timedelta(days=1)


def obter_hostname_por_ip(ip):
    """
    Obtém o nome do host correspondente a um endereço IP.

    Args:
        ip (str): O endereço IP para o qual se deseja obter o nome do host.

    Returns:
        str: O nome do host correspondente ao endereço IP fornecido.

    Esta função tenta obter o nome do host correspondente a um endereço IP usando a função 
    'gethostbyaddr' do módulo 'socket'. Se o nome do host for encontrado, ele é retornado.
    Se o endereço IP for inválido ou o nome do host não puder ser encontrado, são retornadas
    mensagens correspondentes.

    Exemplos:
    >>> obter_hostname_por_ip('192.168.1.1')
    'router.example.com'
    >>> obter_hostname_por_ip('256.0.0.1')
    'Endereço IP inválido'
    >>> obter_hostname_por_ip('invalid_ip')
    'Endereço IP inválido'
    """
    try:
        hostname = socket.gethostbyaddr(ip[:-10])
        return hostname[0]  # O nome do host está na primeira posição da tupla retornada
    except socket.herror:
        return "Hostname não encontrado"
    except socket.gaierror:
        return "Endereço IP inválido"
