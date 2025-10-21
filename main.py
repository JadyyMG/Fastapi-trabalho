from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from bson import ObjectId
import shutil
import os

# Conexão com MongoDB
client = MongoClient("mongodb://localhost:27017")  # COLE AQUI A URL DO MONGO 
db = client["voluntariado_db"]
projetos_collection = db["projetos"]
voluntarios_collection = db["voluntarios"]

# Criação da pasta de uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FastAPI app
app = FastAPI(title="API Voluntariado")

# classes
class Projeto(BaseModel):
    nome: str
    descricao: str
    data_inicio: str
    data_fim: str
    imagem: str = None

class Voluntario(BaseModel):
    nome: str
    email: str
    telefone: str = None
    projetos_inscritos: List[str] = []

# Função utilitária para converter ObjectId
def to_dict(obj):
    obj["id"] = str(obj["_id"])
    del obj["_id"]
    return obj

# ---------------- Projetos ----------------
@app.post("/projetos/")
def criar_projeto(projeto: Projeto):
    result = projetos_collection.insert_one(projeto.dict())
    return {"id": str(result.inserted_id)}

@app.get("/projetos/")
def listar_projetos():
    projetos = list(projetos_collection.find())
    return [to_dict(p) for p in projetos]

@app.get("/projetos/{id}")
def buscar_projeto(id: str):
    projeto = projetos_collection.find_one({"_id": ObjectId(id)})
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return to_dict(projeto)

# ---------------- Voluntários ----------------
@app.post("/voluntarios/")
def criar_voluntario(vol: Voluntario):
    result = voluntarios_collection.insert_one(vol.dict())
    return {"id": str(result.inserted_id)}

@app.get("/voluntarios/")
def listar_voluntarios():
    vols = list(voluntarios_collection.find())
    return [to_dict(v) for v in vols]

# ---------------- Inscrição ----------------
@app.post("/inscrever/{vol_id}/{proj_id}")
def inscrever_voluntario(vol_id: str, proj_id: str):
    vol = voluntarios_collection.find_one({"_id": ObjectId(vol_id)})
    proj = projetos_collection.find_one({"_id": ObjectId(proj_id)})
    if not vol or not proj:
        raise HTTPException(status_code=404, detail="Voluntário ou Projeto não encontrado")
    
    if proj_id not in vol.get("projetos_inscritos", []):
        voluntarios_collection.update_one(
            {"_id": ObjectId(vol_id)},
            {"$push": {"projetos_inscritos": proj_id}}
        )
    return {"message": f"Voluntário {vol['nome']} inscrito no projeto {proj['nome']}"}

# ---------------- Upload de imagem ----------------
@app.post("/upload/{tipo}/{id}")
def upload_arquivo(tipo: str, id: str, arquivo: UploadFile = File(...)):
    caminho = os.path.join(UPLOAD_DIR, arquivo.filename)
    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)
    
    if tipo == "projeto":
        projetos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"imagem": caminho}})
    elif tipo == "voluntario":
        voluntarios_collection.update_one({"_id": ObjectId(id)}, {"$set": {"imagem": caminho}})
    else:
        raise HTTPException(status_code=400, detail="Tipo deve ser projeto ou voluntario")
    
    return {"filename": arquivo.filename}

# ---------------- Download de imagem ----------------
@app.get("/uploads/{filename}")
def get_file(filename: str):
    caminho = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(caminho):
        return FileResponse(caminho)
    raise HTTPException(status_code=404, detail="Arquivo não encontrado")
