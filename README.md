# AWS Tools (Python)
## Rodando o projeto
### Para executar o projeto é preciso ter instalado o Poetry:
- No Linux/macOS:<br>
```curl -sSL https://install.python-poetry.org | python3 -```
- No Windows, você pode usar o PowerShell:<br>
```(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python```

### Após instalado você poderá executar o projeto com o comando:
```poetry run python awstools/nome_do_arquivo.py```<br><br>
**OBS**: (Altere o nome do arquivo para o qual deseja usar, sempre colocando nesse formato: awstools/nome_do_arquivo.py)

## Scripts
- **DynamoDB** <br> Leitura de dados de uma tabela do DynamoDB e inserção em uma outra tabela de outra conta da AWS.
- **SQS** <br> Leitura de dados de uma fila SQS e inserção em uma outra fila de outra conta da AWS.