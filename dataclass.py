from dataclasses import dataclass
from enum import Enum

class StatusEnum(Enum):
    AGENDADO = "Agendado"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"

class TipoEnum(Enum):
    AULA = "Aula"
    REUNIAO = "Reunião"
    TAREFA_COM_PRAZO = "Tarefa com prazo"

class TipoData:
    day: int
    month: int
    year: int

    def __init__(self, day: int, month: int, year: int):
        self.day = day
        self.month = month
        self.year = year

    def date_to_string(self) -> str:
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

@dataclass
class Compromisso:
    data: TipoData
    horario: str
    tipo: TipoEnum
    descricao: str
    status: StatusEnum
    observacoes: str

    def __init__(self, data: TipoData, horario: str, tipo: str, descricao: str, status: str, observacoes: str):
        self.data = data
        self.horario = horario
        self.tipo = TipoEnum(tipo)
        self.descricao = descricao
        self.status = StatusEnum(status)
        self.observacoes = observacoes
        