# B2Broker django-rest-api

## Task

```text
Task:
Develop REST API server using django-rest-framework with pagination, sorting and filtering for two models:

Transaction (id, wallet_id (fk), txid, amount);

Wallet (id, label, balance);

Where txid is required unique string field, amount is a number with 18-digits precision, label is a string field, balance is a summary of all transactions’s amounts. Transaction amount may be negative. Wallet balance should NEVER be negative

Tech Stack:

Python – 3.11+
Database – mysql
API specification – JSON:API — A specification for building APIs in JSON (you are free to use plugin https://django-rest-framework-json-api.readthedocs.io/en/stable/)

Will be your advantage:

Test coverage
SQLAlchemy migrations is an option
Any linter usage
Quick start app guide if you create your own docker-compose or Dockerfiles
Comments in non-standart places in code
Use database indexes if you think it's advisable
Leave github link to repo. Please delete the repo after HR feedback

[execution time limit] 4 seconds (sh)

[memory limit] 1 GB
```

## Requirements

```markdown
Python>=3.11
djangorestframework==3.15.2
python-dotenv==1.0.1
mysqlclient==2.2.4
drf-yasg==1.21.7
mypy==1.10.1
```

### Startup

#### Docker

Needs to set environment variables on root of project directory (file with `.env`), it's required
to run in docker container. All required variables set in `env.example`

Running in docker containers

```bash
make run
```

#### Local

If you have local mysql instance, you can run on host, needs to copy `.env` file in `dev/` directory
because it's folder setup as loading for local development

Install requirements.txt on your directory (before run install command - activate virtual environment)

```bash
pip install -r requirements.txt
```

And run application

```bash
make local-up
```

----

### API specification:

made by `drf-yarg`, available on `${HOST}:${PORT}/api/swagger`

#### Filtering

```markdown
Wallet:
by label - get wallets, where wallet label contains specific word
by balance_from - get wallets by amount, where wallet balance greater or equals set balance

Transaction:
by wallet_id - get all transactions for specific wallet,
by txid - get transaction with specific txid,
by amount_from - get transactions, where transaction amount greater or equals set amount
```

#### Order by

```markdown
Wallet:
order by balance (desc/asc)

Transaction:
order by amount (desc/asc)
```

___

### Linter

Used mypy