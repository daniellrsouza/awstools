import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Credenciais e nomes dos buckets
origem_bucket = "unload.loadshark.io"
destino_bucket = "unload-braskem-pacey"

# Clientes S3 para as duas contas (substitua pelos perfis configurados)
s3_origem = boto3.Session(profile_name="loadshark").client("s3")
s3_destino = boto3.Session(profile_name="pacey").client("s3")

try:
    continuation_token = None  # Token para paginação
    objetos_migrados = 0  # Contador de objetos migrados

    # Loop para listar todos os objetos do bucket de origem paginadamente
    while True:
        # Listar objetos com paginação
        if continuation_token:
            response = s3_origem.list_objects_v2(Bucket=origem_bucket, ContinuationToken=continuation_token)
        else:
            response = s3_origem.list_objects_v2(Bucket=origem_bucket)

        objetos = response.get("Contents", [])

        # Verificar se há objetos na resposta
        if not objetos:
            print("Nenhum objeto encontrado no bucket de origem.")
            break

        # Copiar cada objeto do bucket de origem para o bucket de destino
        for obj in objetos:
            copy_source = {"Bucket": origem_bucket, "Key": obj["Key"]}
            print(f"Copiando {obj['Key']}...")

            s3_destino.copy_object(
                CopySource=copy_source, Bucket=destino_bucket, Key=obj["Key"]
            )
            objetos_migrados += 1

        # Verificar se há uma próxima página
        if response.get("IsTruncated"):  # Se a resposta foi truncada, há mais páginas
            continuation_token = response.get("NextContinuationToken")
        else:
            break  # Todas as páginas foram processadas

    print(f"Migração concluída com sucesso! Total de objetos migrados: {objetos_migrados}")

except (NoCredentialsError, PartialCredentialsError) as e:
    print(f"Erro de credenciais: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
