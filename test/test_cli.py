import unittest
from unittest.mock import patch, MagicMock
from main.error import PSBaseError
from main.domain import FichaAnalise, Risco, Paciente, Atendimento
from main.cli import TerminalClient


class TestCLI(unittest.TestCase):
    def setUp(self):
        """ Configuração inicial para os testes """
        self.ps_service_mock = MagicMock()
        self.cli = TerminalClient(self.ps_service_mock)

    # --- TESTES PARA REGISTRAR ATENDIMENTO ---
    @patch("builtins.input", side_effect=["12345678900"])
    def test_paciente_nao_cadastrado(self, mock_input):
        """ Testa se um paciente não cadastrado exibe mensagem de erro ao registrar atendimento """
        self.ps_service_mock.pacientes.buscar.return_value = None

        with patch("builtins.print") as mock_print:
            self.cli.registrar_atendimento()
            mock_print.assert_any_call("\nPaciente não encontrado.")

    @patch("builtins.input", side_effect=[
        "12345678900",
        "sim", "não", "não", "não"
    ])
    def test_paciente_risco_morte(self, mock_input):
        """ Testa se o paciente com risco de morte é classificado corretamente """
        paciente_mock = MagicMock()
        self.ps_service_mock.pacientes.buscar.return_value = paciente_mock
        self.ps_service_mock.classificar_risco.return_value = Risco.VERMELHO

        with patch("builtins.print") as mock_print:
            self.cli.registrar_atendimento()
            mock_print.assert_any_call("\nClassificação de risco: VERMELHO")

    @patch("builtins.input", side_effect=[
        "12345678900",
        "não", "sim", "não", "não"
    ])
    def test_paciente_gravidade_alta(self, mock_input):
        """ Testa se o paciente com gravidade alta é classificado corretamente """
        paciente_mock = MagicMock()
        self.ps_service_mock.pacientes.buscar.return_value = paciente_mock
        self.ps_service_mock.classificar_risco.return_value = Risco.LARANJA

        with patch("builtins.print") as mock_print:
            self.cli.registrar_atendimento()
            mock_print.assert_any_call("\nClassificação de risco: LARANJA")

    @patch("builtins.input", side_effect=[
        "12345678900",
        "não", "não", "sim", "não"
    ])
    def test_paciente_gravidade_moderada(self, mock_input):
        """ Testa se o paciente com gravidade moderada é classificado corretamente """
        paciente_mock = MagicMock()
        self.ps_service_mock.pacientes.buscar.return_value = paciente_mock
        self.ps_service_mock.classificar_risco.return_value = Risco.AMARELO

        with patch("builtins.print") as mock_print:
            self.cli.registrar_atendimento()
            mock_print.assert_any_call("\nClassificação de risco: AMARELO")

    @patch("builtins.input", side_effect=[
        "12345678900",
        "não", "não", "não", "sim"
    ])
    def test_paciente_gravidade_baixa(self, mock_input):
        """ Testa se o paciente com gravidade baixa é classificado corretamente """
        paciente_mock = MagicMock()
        self.ps_service_mock.pacientes.buscar.return_value = paciente_mock
        self.ps_service_mock.classificar_risco.return_value = Risco.VERDE

        with patch("builtins.print") as mock_print:
            self.cli.registrar_atendimento()
            mock_print.assert_any_call("\nClassificação de risco: VERDE")

    @patch("builtins.input", side_effect=[
        "12345678900",
        "não", "não", "não", "não"
    ])
    def test_paciente_sem_gravidade(self, mock_input):
        """ Testa se o paciente sem gravidade é classificado corretamente """
        paciente_mock = MagicMock()
        self.ps_service_mock.pacientes.buscar.return_value = paciente_mock
        self.ps_service_mock.classificar_risco.return_value = Risco.AZUL

        with patch("builtins.print") as mock_print:
            self.cli.registrar_atendimento()
            mock_print.assert_any_call("\nClassificação de risco: AZUL")

    @patch("builtins.input", side_effect=["12345678900"])
    def test_erro_ao_registrar_atendimento(self, mock_input):
        """ Testa se um erro ao buscar paciente é tratado corretamente """
        self.ps_service_mock.pacientes.buscar.side_effect = PSBaseError("Erro ao buscar paciente.")

        with patch("builtins.print") as mock_print:
            self.cli.registrar_atendimento()
            mock_print.assert_any_call("\nErro ao registrar atendimento: Erro ao buscar paciente.")

    # --- TESTES PARA HISTÓRICO DE ATENDIMENTO ---
    @patch("builtins.input", side_effect=["12345678900"])
    def test_buscar_historico_cpf_valido(self, mock_input):
        """ Testa se um CPF válido retorna o histórico de atendimentos """
        paciente_mock = MagicMock()
        paciente_mock.nome = "João da Silva"
        self.ps_service_mock.pacientes.buscar.return_value = paciente_mock

        atendimento_mock = [MagicMock(), MagicMock()]  # Simulando dois atendimentos
        self.ps_service_mock.buscar_historico.return_value = atendimento_mock

        with patch("builtins.print") as mock_print:
            self.cli.buscar_historico()
            mock_print.assert_any_call(f"\nHistórico de atendimentos para {paciente_mock.nome}:")

    @patch("builtins.input", side_effect=["12345678900"])
    def test_buscar_historico_cpf_nao_cadastrado(self, mock_input):
        """ Testa se um CPF não cadastrado exibe a mensagem de erro apropriada """
        self.ps_service_mock.pacientes.buscar.return_value = None

        with patch("builtins.print") as mock_print:
            self.cli.buscar_historico()
            mock_print.assert_any_call("\nPaciente não encontrado.")

if __name__ == "__main__":
    unittest.main()
