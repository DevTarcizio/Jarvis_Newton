import gspread, datetime
from google.oauth2.service_account import Credentials

escopo = [
    "https://www.googleapis.com/auth/spreadsheets",
]

credentials = Credentials.from_service_account_file("credentials.json", scopes=escopo)
client = gspread.authorize(credentials)

ID_SHEETS = "1_TxiLg264n0wU6K38bZgdmiMEm-jJYKQ2ejsjeIt1_Q"

# Lógica Principal
def read_data():
    try:
        planilha = client.open_by_key(ID_SHEETS)
        aba = planilha.sheet1

        compromissos_diários = []
        compromissos_semanais = []
        compromissos_mensais = []

        registros = aba.get_all_records(head=2, expected_headers=["Data", "Horário", "Tipo", "Descrição", "Status", "Observações"])      
        for registro in registros:
            data_registro = datetime.datetime.strptime(registro["Data"], "%d/%m/%Y").date()

            if data_registro == datetime.date.today():
                compromissos_diários.append(registro)

            elif data_registro <= datetime.date.today() + datetime.timedelta(days=6):
                compromissos_semanais.append(registro)

            elif data_registro.month == datetime.date.today().month and data_registro >= datetime.date.today():
                compromissos_mensais.append(registro)

    except gspread.exceptions.APIError as api_error:
        print(f"Erro na API do Google Sheets: {api_error}")

    except Exception as e:
        print(f"Erro ao acessar a planilha: {e}")

def write_data(data):
    try:
        planilha = client.open_by_key(ID_SHEETS)
        aba = planilha.sheet1

        # Adiciona os dados na próxima linha disponível
        aba.append_row(data)

    except gspread.exceptions.APIError as api_error:
        print(f"Erro na API do Google Sheets: {api_error}")

    except Exception as e:
        print(f"Erro ao acessar a planilha: {e}")

if __name__ == "__main__":
    read_data()
    print()