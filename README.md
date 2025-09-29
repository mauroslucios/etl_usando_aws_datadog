# ETL Motivo de Decisão

Este projeto implementa um processo **ETL (Extract, Transform, Load)** utilizando **PySpark**, **MySQL**, **MongoDB** e **LocalStack (S3)** para simular a integração de dados e armazenamento de resultados de análises de crédito.

## 📌 Objetivo

O pipeline executa as seguintes etapas:
1. **Extração** de dados de tabelas relacionais (MySQL).
2. **Transformação** aplicando regras de negócio:
   - Cliente deve morar em zona **rural**;
   - Tipo de pessoa: **PF**;
   - Soma dos bens (`valor_total_bens`) **>= 300.000**;
   - Não estar negativado.
3. **Carga** dos resultados:
   - Arquivos **JSON particionados** em um bucket S3 (via LocalStack).
   - Opcionalmente, grava em **MySQL** e **MongoDB**.

---

## 🚀 Tecnologias Utilizadas

- [Python 3.11](https://www.python.org/)
- [PySpark](https://spark.apache.org/)
- [MySQL](https://www.mysql.com/)
- [MongoDB](https://www.mongodb.com/)
- [LocalStack](https://localstack.cloud/)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) (SDK AWS em Python)

---

## 📂 Estrutura do Projeto

```
.
├── etl_motivo_decisao.py   # Script principal (orquestração do ETL)
├── ETL.py                  # Classe ETL (extração, transformação, carga)
├── ETLLogger.py            # Classe para logs estruturados
├── logs/
│   └── etl.log             # Arquivo de logs gerados
├── jars/
│   └── mysql-connector-j-8.0.33.jar
└── README.md
```

---

## ⚙️ Pré-requisitos

- Docker e Docker Compose
- LocalStack rodando localmente
- MySQL e MongoDB ativos (em containers ou serviços externos)
- Variáveis de ambiente configuradas (padrão já incluso no código):
  ```bash
  MYSQL_URL=jdbc:mysql://172.22.1.2:3306/elysium
  MYSQL_USER=root
  MYSQL_PASSWORD=123456
  MONGO_URI=mongodb://172.15.0.3:27017/elysium_db
  LOCALSTACK_ENDPOINT=http://localhost:4566
  S3_BUCKET=motivo-de-decisao
  S3_PREFIX=analises/
  ```

---

## ▶️ Como Executar

1. **Subir o LocalStack:**
   ```bash
   docker-compose up -d localstack
   ```

2. **Executar o ETL:**
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
   export PATH=$JAVA_HOME/bin:$PATH
   spark-submit --jars mysql-connector-j-8.0.33.jar main.py
   ```

3. **Verificar logs:**
   ```bash
   tail -f logs/etl.log
   ```

---

## 📦 Exemplos de Uso (S3 via LocalStack)

### Listar arquivos gerados no bucket:
```bash
awslocal s3 ls s3://motivo-de-decisao/analises/
```

### Baixar um arquivo de análise:
```bash
awslocal s3 cp s3://motivo-de-decisao/analises/part-00000.json .
```

### Visualizar o conteúdo:
```bash
cat part-00000.json | jq .
```

---

## 📝 Estrutura de Log

Cada ação do ETL é registrada no arquivo `logs/etl.log` com:
- **timestamp**
- **evento**
- **banco/tabela**
- **ação**
- **resultado**
- **erro (se houver)**

Exemplo:
```
2025-09-27 22:15:03,245 - INFO - [Extração de tabela] Database: elysium Table: cliente Action: Lendo dados Result: Sucesso
2025-09-27 22:15:07,892 - ERROR - [Carga no S3] Database: motivo-de-decisao Table: analises Action: Upload Result: Erro Error: ...
```

---

## 📌 Próximos Passos

- Adicionar testes unitários (PyTest).
- Melhorar performance da escrita em S3 (uso de `coalesce` ou `repartition`).
- Criar docker-compose para orquestrar Spark + MySQL + Mongo + LocalStack.

![LocalStack](https://github.com/mauroslucios/etl_usando_aws_datadog/issues/5#issue-3463030524)