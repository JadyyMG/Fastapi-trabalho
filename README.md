# API FastAPI de Voluntariado

API para gerenciamento de projetos de voluntariado usando **FastAPI** e **MongoDB**.  
Perfeita para consumo por **frontend em React**.

---

## Pré-requisitos

- Python 3.10 ou superior
- MongoDB (local ou Atlas)
- Node/React (frontend)
- Git (para clonar o repositório)

---

## Instalação da API

1. Clone o repositório:
```
git clone https://github.com/JadyyMG/Fastapi-trabalho.git
cd Fastapi-trabalho
```
2.Crie e ative o ambiente virtual:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```
3.Instale:
```
python -m pip install --upgrade pip
python -m pip install fastapi "uvicorn[standard]" pymongo python-multipart
```
4.Configurar MongoDB

 No MongoDB local:

  Certifique-se que o serviço está rodando: mongod

MongoDB Atlas:

  Substitua a parte pela URI em main.py:
Ex:
```
client = MongoClient("sua_uri_do_mongodb")
```
---
## Rodar a API

Copie o código:
```
python -m uvicorn main:app --reload
```

Abra no navegador:
Swagger Docs: http://127.0.0.1:8000/docs

Endpoint raiz: http://127.0.0.1:8000/

---

## Endpoints disponíveis
Isso vocês que fizeram o software devem saber responder no dia do trabalho !!

Projetos
```
GET /projetos/ → Lista todos os projetos

POST /projetos/ → Cria projeto

Ex:
  "nome": "Limpeza de Praia",
  "descricao": "Coleta de lixo na praia central",
  "data_inicio": "2025-11-01",
  "data_fim": "2025-11-02"

GET /projetos/{id} → Retorna projeto por ID
```
Voluntários
```
GET /voluntarios/ → Lista todos os voluntários com projetos inscritos

POST /voluntarios/ → Cria voluntário

Ex:
  "nome": "Jadilson",
  "email": "jadilson@email.com",
  "telefone": "11999999999"

GET /voluntarios/{id} → Retorna voluntário por ID
```
Inscrição
```
POST /inscrever/{vol_id}/{proj_id} → Inscreve um voluntário em um projeto
```
Upload de imagens
```
POST /upload/{tipo}/{id} → Upload de imagem para projeto ou voluntario

GET /uploads/{filename} → Baixar imagem
