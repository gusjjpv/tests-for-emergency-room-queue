from main.cli import TerminalClient
from main.repository import PacienteRepository, AtendimentoRepository
from main.service import ProntoSocorroService

if __name__ == '__main__':
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    ps_service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(ps_service)
    cli.executar()