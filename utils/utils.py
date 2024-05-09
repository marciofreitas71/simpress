def insere_dados_csv_to_bd():
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