import boto3

# Configurar os perfis das contas
session_origem = boto3.Session(profile_name='nome_perfil_origem', region_name='us-east-1')
session_destino = boto3.Session(profile_name='nome_perfil_destino', region_name='us-east-1')

# Conectar ao DynamoDB em cada conta usando os perfis
dynamodb_origem = session_origem.resource('dynamodb')
dynamodb_destino = session_destino.resource('dynamodb')

# Definir as tabelas de origem e destino
table_origem = dynamodb_origem.Table('nome_tabela_origem')
table_destino = dynamodb_destino.Table('nome_tabela_destino')

# Função para migrar dados
def migrar_dados():
    # Realizar a varredura completa da tabela de origem
    response = table_origem.scan()
    items = response['Items']
    print(len(items))

    # Inserir dados na tabela de destino
    with table_destino.batch_writer() as batch:
        for item in items:
            print(item)
            batch.put_item(Item=item)

    # Continuar a varredura enquanto houver mais dados
    while 'LastEvaluatedKey' in response:
        response = table_origem.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items = response['Items']
        print(len(items))
        with table_destino.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    print('finalizou')

# Executar a migração
migrar_dados()
