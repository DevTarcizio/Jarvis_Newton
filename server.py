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

    new_data = TipoData(0, 0, 0)

    new_data.day = int(data["data"].split("/")[0])
    new_data.month = int(data["data"].split("/")[1])
    new_data.year = int(data["data"].split("/")[2])

    compromisso = Compromisso(
        data=new_data,
        horario=data["horario"],
        tipo=data["tipo"],
        descricao=data["descricao"],
        status=data["status"],
        observacoes=data["observacoes"]
    )

    write_data(compromisso)

    return {"status": "success"}