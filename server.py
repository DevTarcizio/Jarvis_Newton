from fastapi import FastAPI
from dataclass import TipoData, Compromisso
from sheets import write_data

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/webhook")
def webhook(data: dict):
    print("Dados recebidos do webhook:", data)

    new_data : TipoData = {}

    new_data.day = data["data"].split("/")[0]
    new_data.month = data["data"].split("/")[1]
    new_data.year = data["data"].split("/")[2]

    compromisso : Compromisso = {}
    compromisso.data = new_data
    compromisso.horario = data["horario"]
    compromisso.tipo = data["tipo"]
    compromisso.descricao = data["descricao"]
    compromisso.status = data["status"]
    compromisso.observacoes = data["observacoes"]

    write_data(compromisso)

    return {"status": "success"}