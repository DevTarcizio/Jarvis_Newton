import gspread, datetime, os, json
from google.oauth2.service_account import Credentials
from dataclass import Compromisso, TipoEnum, StatusEnum

escopo = [
    "https://www.googleapis.com/auth/spreadsheets",
]

google_string = os.getenv("GOOGLE_CREDENTIALS")
google_credentials = json.loads(google_string)

credentials = Credentials.from_service_account_info(google_credentials, scopes=escopo)
client = gspread.authorize(credentials)

ID_SHEETS = "1_TxiLg264n0wU6K38bZgdmiMEm-jJYKQ2ejsjeIt1_Q"

# Lógica Principal
def read_data():
    compromissos_diários = []
    compromissos_semanais = []
    compromissos_mensais = []

    try:
        planilha = client.open_by_key(ID_SHEETS)
        aba = planilha.sheet1

        dia_atual = datetime.date.today()

        registros = aba.get_all_records(head=2, expected_headers=["Data", "Horário", "Tipo", "Descrição", "Status", "Observações"])      
        for registro in registros:
            data_registro = datetime.datetime.strptime(registro["Data"], "%d/%m/%Y").date()

            if data_registro == dia_atual:
                compromissos_diários.append(registro)

            elif data_registro <= dia_atual + datetime.timedelta(days=6):
                compromissos_semanais.append(registro)

            elif data_registro.month == dia_atual.month and data_registro >= dia_atual:
                compromissos_mensais.append(registro)

    except gspread.exceptions.APIError as api_error:
        print(f"Erro na API do Google Sheets: {api_error}")

    except Exception as e:
        print(f"Erro ao acessar a planilha: {e}")

    return compromissos_diários, compromissos_semanais, compromissos_mensais

def write_data(data: Compromisso):
    try:
        planilha = client.open_by_key(ID_SHEETS)
        aba = planilha.sheet1

        # Adiciona os dados na próxima linha disponível
        aba.append_row([data.data.date_to_string(), data.horario, data.tipo.value, data.descricao, data.status.value, data.observacoes])

    except gspread.exceptions.APIError as api_error:
        print(f"Erro na API do Google Sheets: {api_error}")

    except Exception as e:
        print(f"Erro ao acessar a planilha: {e}")

if __name__ == "__main__":
    read_data()
    print()