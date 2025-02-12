import heapq
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from main.error import *


@dataclass
class Paciente:
    """
    Representa um paciente no sistema.

    Attributes:
        nome: Nome completo do paciente.
        cpf: CPF do paciente (no formato 11111111111, com 11 dígitos numéricos).
        email: E-mail do paciente.
        nascimento: Data de nascimento do paciente (no formato DD/MM/YYYY).
    """
    nome: str
    cpf: str
    email: str
    nascimento: str

    def __post_init__(self):
        self.validar_nome(self.nome)
        self.validar_cpf(self.cpf)
        self.validar_email(self.email)

    def validar_nome(self, nome: str) -> str:
        if not nome or not nome.strip():
            raise ValidacaoError("O nome do paciente é obrigatório.")
        if not re.match(r"^[a-zA-ZÀ-ú\s]+$", nome):
            raise ValidacaoError("O nome do paciente contém caracteres inválidos.")
        return nome.strip()

    def validar_cpf(self, cpf: str) -> str:
        cpf = re.sub(r"[^0-9]", "", cpf)  # Remove caracteres não numéricos
        if not cpf.isdigit():
            raise ValidacaoError("CPF inválido, deve conter 11 dígitos numéricos.")
        return cpf

    def validar_email(self, email: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValidacaoError("E-mail inválido.")
        return email

    def validar_nascimento(self, nascimento: str) -> str:
        try:
            data = datetime.strptime(nascimento, "%d/%m/%Y")
            if data > datetime.now():
                raise ValidacaoError("A data de nascimento não pode ser futura.")
            return nascimento
        except ValueError:
            raise ValidacaoError("Data de nascimento inválida, use o formato DD/MM/YYYY.")

    def __str__(self):
        return f'Paciente: {self.nome} ({self.cpf})'

class Risco(Enum):
    """
    Enumeração que representa os níveis de risco de um paciente, conforme o protocolo de Manchester.

    Valores:
        VERMELHO: Risco de morte iminente.
        LARANJA: Risco alto.
        AMARELO: Risco moderado.
        VERDE: Risco baixo.
        AZUL: Risco muito baixo.
    """
    VERMELHO = 1
    LARANJA  = 2
    AMARELO  = 3
    VERDE    = 4
    AZUL     = 5

@dataclass
class FichaAnalise:
    """
    Representa a ficha de análise de um paciente durante a triagem.

    Attributes:
        risco_morte: Indica se o paciente corre risco de morte.
        gravidade_alta: Indica se o paciente tem gravidade alta.
        gravidade_moderada: Indica se o paciente tem gravidade moderada.
        gravidade_baixa: Indica se o paciente tem gravidade baixa.
    """
    risco_morte: bool
    gravidade_alta: bool
    gravidade_moderada: bool
    gravidade_baixa: bool

@dataclass
class Atendimento:
    """
    Representa um atendimento de um paciente no pronto-socorro.

    Attributes:
        paciente: O paciente associado ao atendimento.
        risco: Nível de risco do paciente.
        entrada: Data e hora de entrada do paciente no sistema.
    """
    paciente: Paciente
    risco: Risco
    entrada: datetime = datetime.now()

    def __str__(self):
        return f"Atendimento:\nPaciente: {self.paciente}\nRisco: {self.risco.name}\nEntrada: {self.entrada.strftime('%d/%m/%Y %X')}"

class FilaAtendimento:
    """
    Gerencia a fila de atendimento dos pacientes, priorizando por nível de risco.
    """
    def __init__(self):
        self.fila = []

    def inserir(self, atendimento: Atendimento):
        heapq.heappush(self.fila, (atendimento.risco.value, atendimento))

    def proximo(self):
        if len(self.fila) == 0:
            raise FilaVaziaError('Não tem nenhum paciente na fila de atendimento')
        return heapq.heappop(self.fila)[1]

    def possui_proximo(self):
        return len(self.fila) > 0

    def tamanho(self):
        return len(self.fila)

