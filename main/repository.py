from typing import List

from main.domain import Paciente, Atendimento

from main.error import CPFDuplicadoError, PacienteNaoCadastradoError

class PacienteRepository:
    """
    Gerencia o armazenamento e recuperação de pacientes no sistema (apenas em memória).
    """
    def __init__(self):
        self.pacientes: List[Paciente] = []

    def inserir(self, paciente: Paciente):
        self.pacientes.append(paciente)

    def buscar(self, cpf: str):
        for p in self.pacientes:
            if p.cpf == cpf:
                return p
        return None

class AtendimentoRepository:
    """
    Gerencia o armazenamento e recuperação de atendimentos no sistema (apenas em memória).
    """
    def __init__(self, paciente_repository: PacienteRepository):
        self.paciente_repository = paciente_repository
        self.atendimentos: List[Atendimento] = []

    def inserir(self, atendimento: Atendimento):
        if self.paciente_repository.buscar(atendimento.paciente.cpf) == None:
            raise PacienteNaoCadastradoError('Paciente não cadastrado')
        else:
            self.atendimentos.append(atendimento)

    def historico_atendimentos(self, cpf: str):
        historico = []
        if self.paciente_repository.buscar(cpf) == None:
            raise PacienteNaoCadastradoError('Paciente não cadastrado')
        else:
            for i in range(0, len(self.atendimentos) - 1):
                if self.atendimentos[i].paciente.cpf == cpf:
                    historico.append(self.atendimentos[i])
            return historico