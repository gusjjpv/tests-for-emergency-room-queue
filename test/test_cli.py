import unittest
from unittest.mock import patch, MagicMock
from main.error import PSBaseError
from main.domain import FichaAnalise, Risco, Paciente
from main.cli import TerminalClient


class TestRegistrarAtendimento(unittest.TestCase):
    def setUp(self):
        """ Configuração inicial: mock do serviço e inicialização do TerminalClient """
        self.ps_service_mock = MagicMock()
        self.cli = TerminalClient(self.ps_service_mock)

    @patch("builtins.input", side_effect=["12345678900"])
    def test_paciente_nao_cadastrado(self, mock_input):
        """ Testa se um paciente não cadastrado exibe mensagem de erro """
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

if __name__ == "__main__":
    unittest.main()
