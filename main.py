import telebot, threading, time, os, requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
MY_CHAT_ID = "5387408149"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message:telebot.types.Message):
    bot.reply_to(message, "Olá, sou o Jarvis Newton, como posso te ajudar")


@bot.message_handler(commands=['novo_compromisso'])
def novo_compromisso(message:telebot.types.Message):
    bot.reply_to(message, "Para criar um novo compromisso, por favor, forneça os detalhes no seguinte formato:\n"
                          "Data (dd/mm/aaaa), Horário (hh:mm), Tipo (Aula/Reunião/Tarefa com prazo), "
                          "Descrição, Status (Agendado/Em andamento/Concluído/Cancelado), Observações")

    bot.register_next_step_handler(message, process_compromisso)

def process_compromisso(message:telebot.types.Message):
    text = message.text
    chat_id = message.chat.id

    dados_limpos = [item.strip() for item in text.split(",")]

    payload = {
        "data" : dados_limpos[0],
        "horario" : dados_limpos[1],
        "tipo" : dados_limpos[2],
        "descricao" : dados_limpos[3],
        "status" : dados_limpos[4],
        "observacoes" : dados_limpos[5],
        "chat_id" : chat_id
    }

    url = "https://jarvis-newton.onrender.com/webhook"

    resposta = requests.post(url, json=payload)

    if (resposta.status_code == 200):
        bot.reply_to(message, "Compromisso enviado com sucesso!")
    else:
        bot.reply_to(message, "Ocorreu um erro ao enviar o compromisso. Por favor, tente novamente.")

def send_daily_resume(compromissos: list):

    if compromissos is None or len(compromissos) == 0:
        bot.send_message(MY_CHAT_ID, "Nenhum compromisso encontrado para hoje.")
        return

    message = "Agenda Diária:\n\n"

    for compromisso in compromissos:
        message += f"Data: {compromisso['Data']}\n"
        message += f"Horário: {compromisso['Horário']}\n"
        message += f"Tipo: {compromisso['Tipo']}\n"
        message += f"Descrição: {compromisso['Descrição']}\n"
        message += f"Status: {compromisso['Status']}\n"
        message += f"Observações: {compromisso['Observações']}\n\n"

    bot.send_message(MY_CHAT_ID, message)

def send_weekly_resume(compromissos: list):

    if compromissos is None or len(compromissos) == 0:
        bot.send_message(MY_CHAT_ID, "Nenhum compromisso encontrado para esta semana.")
        return

    message = "Agenda Semanal:\n\n"

    for compromisso in compromissos:
        message += f"Data: {compromisso['Data']}\n"
        message += f"Horário: {compromisso['Horário']}\n"
        message += f"Tipo: {compromisso['Tipo']}\n"
        message += f"Descrição: {compromisso['Descrição']}\n"
        message += f"Status: {compromisso['Status']}\n"
        message += f"Observações: {compromisso['Observações']}\n\n"

    bot.send_message(MY_CHAT_ID, message)

def send_monthly_resume(compromissos: list):

    if compromissos is None or len(compromissos) == 0:
        bot.send_message(MY_CHAT_ID, "Nenhum compromisso encontrado para este mês.")
        return

    message = "Agenda Mensal:\n\n"

    for compromisso in compromissos:
        message += f"Data: {compromisso['Data']}\n"
        message += f"Horário: {compromisso['Horário']}\n"
        message += f"Tipo: {compromisso['Tipo']}\n"
        message += f"Descrição: {compromisso['Descrição']}\n"
        message += f"Status: {compromisso['Status']}\n"
        message += f"Observações: {compromisso['Observações']}\n\n"

    bot.send_message(MY_CHAT_ID, message)

if __name__ == "__main__":
    bot.infinity_polling()
