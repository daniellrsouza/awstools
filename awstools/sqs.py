from dotenv import load_dotenv
import boto3
import botocore.exceptions
import os

load_dotenv()  # Carrega as variáveis do arquivo .env

# Credenciais do novo usuário
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Conta de origem - configurada com as credenciais do outro usuário
session_source = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Conta de origem
sqs_source = session_source.client('sqs', region_name='us-east-1')
queue_url_source = 'queue_url_source'

# Conta de destino
sqs_target = boto3.client('sqs', region_name='us-east-1')
queue_url_target = 'queue_url_target'

def copy_messages():
    while True:
        try:
            # Recebe mensagens da fila original
            response = sqs_source.receive_message(
                QueueUrl=queue_url_source,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10
            )

            if 'Messages' not in response:
                print("Nenhuma mensagem restante.")
                break

            for message in response['Messages']:
                try:
                    # Reenvia a mensagem para a nova fila
                    sqs_target.send_message(
                        QueueUrl=queue_url_target,
                        MessageGroupId='DeliveryServiceProcessFailed',
                        MessageBody=message['Body']
                    )
                    print(f"Mensagem {message['MessageId']} migrada com sucesso.")
                    
                    # Exclui a mensagem da fila original após o envio
                    sqs_source.delete_message(
                        QueueUrl=queue_url_source,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    print(f"Mensagem {message['MessageId']} excluída da fila original.")

                except botocore.exceptions.BotoCoreError as e:
                    # Captura erros relacionados ao envio/exclusão de mensagens
                    print(f"Erro ao processar mensagem {message['MessageId']}: {e}")

        except botocore.exceptions.BotoCoreError as e:
            # Captura erros relacionados à recepção de mensagens da fila original
            print(f"Erro ao receber mensagens da fila: {e}")
            break

# Iniciar a cópia das mensagens
copy_messages()
