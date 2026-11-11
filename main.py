import telebot, threading, time, os, requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
MY_CHAT_ID = "5387408149"

bot = telebot.TeleBot(TOKEN)


def send_message_to_user_every_30_seconds():
    while True:
        try:
            bot.send_message(MY_CHAT_ID, "Olá, estou aqui para te lembrar de algo importante!")
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

        time.sleep(30)  # Aguarda 30 segundos antes de enviar a próxima mensagem


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

if __name__ == "__main__":
    print("Iniciando o Jarvis Newton...")

    bot.infinity_polling()
