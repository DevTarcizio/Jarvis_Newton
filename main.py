import telebot, threading, time, os

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
    bot.set_webhook()

if __name__ == "__main__":
    print("Iniciando o Jarvis Newton...")

    thread_message = threading.Thread(target=send_message_to_user_every_30_seconds, daemon=True)

    thread_message.start()

    bot.infinity_polling()
