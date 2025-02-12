from typing import List

from main.domain import *
from main.repository import PacienteRepository, AtendimentoRepository


class ProntoSocorroService:
    """
    Serviço principal do pronto-socorro, responsável por coordenar as operações do sistema.
    """
    def __init__(self, pacientes: PacienteRepository, atendimentos: AtendimentoRepository):
        self.pacientes = pacientes
        self.atendimentos = atendimentos
        self.fila_atendimento = FilaAtendimento()

    def registrar_paciente(self, nome, cpf, email, nascimento):
        paciente = Paciente(nome, cpf, email, nascimento)
        self.pacientes.inserir(paciente)
        return paciente

    def classificar_risco(self, ficha: FichaAnalise) -> Risco:
        if ficha.risco_morte:
            return Risco.VERMELHO
        if ficha.gravidade_alta:
            return Risco.AMARELO
        if ficha.gravidade_moderada:
            return Risco.LARANJA
        if ficha.gravidade_baixa:
            return Risco.VERDE
        else:
            return Risco.AZUL

    def registrar_atendimento(self, paciente: Paciente, risco: Risco) -> Atendimento:
        atendimento = Atendimento(paciente, risco)
        self.atendimentos.inserir(atendimento)
        return atendimento

    def inserir_fila_atendimento(self, atendimento: Atendimento) -> bool:
        self.fila_atendimento.inserir(atendimento)
        return True

    def chamar_proximo(self) -> Atendimento:
        return self.fila_atendimento.proximo()

    def buscar_historico(self, paciente: Paciente) -> List[Atendimento]:
        return self.atendimentos.historico_atendimentos(paciente.cpf)