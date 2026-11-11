from fastapi import FastAPI
from dataclass import TipoData, Compromisso
from bot_commands import send_daily_resume, send_monthly_resume, send_weekly_resume
from sheets import write_data, read_data

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


@app.get("/cron/resume_daily")
def resume_daily():

    daily_compromissos = read_data()[0]
    send_daily_resume(daily_compromissos)    

    return {"message": "Daily resume endpoint"}


@app.get("/cron/resume_weekly")
def resume_weekly():

    weekly_compromissos = read_data()[1]
    send_weekly_resume(weekly_compromissos)    

    return {"message": "Weekly resume endpoint"}


@app.get("/cron/resume_monthly")
def resume_monthly():

    monthly_compromissos = read_data()[2]
    send_monthly_resume(monthly_compromissos)    

    return {"message": "Monthly resume endpoint"}