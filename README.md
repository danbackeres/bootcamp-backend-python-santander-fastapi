# FastAPI

Projeto em Python de API assíncrona de uma academia para uma competição de crossfit. Projeto destinado a atender ao desafio de Lab.

## Subir o Servidor

Suba o server com este comando:

```
uvicorn workout_api.main:app --reload
```

### Acesse a documentação

A documentação do FastApi fica em:

```
http://127.0.0.1:8000/docs
```

## Ativar o Ambiente Virtual

Abra o terminal e digite:

```
workoutapi\Scripts\activate
```

## Rodar as Migrations

O comando deve estar configurado no `Makefile`

Antes suba o servidor PostgreSQL:

```
docker compose up -d
```

Depois crie as migrations:

```
make create-migrations d="init_db"
```

E por fim rode:

```
make run-migrations
```
