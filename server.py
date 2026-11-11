from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/webhook")
def webhook(data: dict):
    print("Dados recebidos do webhook:", data)
    return {"status": "success", "data": data}