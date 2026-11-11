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

@dataclass
class Compromisso:
    data: TipoData
    horario: str
    tipo: TipoEnum
    descricao: str
    status: StatusEnum
    observacoes: str