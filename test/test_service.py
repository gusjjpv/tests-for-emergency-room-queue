import unittest
import heapq
from main.domain import FilaAtendimento, Atendimento, Paciente, Risco
from main.service import ProntoSocorroService
from main.error import FilaVaziaError

class TestFilaAtendimento(unittest.TestCase):

    def setUp(self):
        """Executa antes de cada teste, inicializando a fila."""
        self.fila = FilaAtendimento()

    def test_fila_vazia(self):
        """Testa se chamar proximo() em uma fila vazia gera a exceção correta."""
        with self.assertRaises(FilaVaziaError) as context:
            self.fila.proximo()
        self.assertEqual(str(context.exception), "Não tem nenhum paciente na fila de atendimento")

    def test_fila_com_pacientes(self):
        """Testa a inserção e ordem de atendimento na fila."""
        paciente1 = Paciente("Ana", "12345678901", "ana@email.com", "01/01/2000")
        paciente2 = Paciente("Bruno", "98765432100", "bruno@email.com", "05/06/1985")
        paciente3 = Paciente("Carlos", "11122233344", "carlos@email.com", "10/10/1995")

        atendimento1 = Atendimento(paciente1, Risco.VERDE)  # Baixa prioridade
        atendimento2 = Atendimento(paciente2, Risco.VERMELHO)  # Alta prioridade
        atendimento3 = Atendimento(paciente3, Risco.AMARELO)  # Prioridade intermediária

        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)
        self.fila.inserir(atendimento3)

        # Verificar se a ordem correta de prioridade está sendo seguida
        self.assertEqual(self.fila.proximo(), atendimento2)
        self.assertEqual(self.fila.proximo(), atendimento3)
        self.assertEqual(self.fila.proximo(), atendimento1)

    def test_possui_proximo(self):
        """Testa se o método possui_proximo() funciona corretamente."""
        self.assertFalse(self.fila.possui_proximo())

        paciente = Paciente("Davi", "99988877766", "davi@email.com", "20/12/1990")
        atendimento = Atendimento(paciente, Risco.LARANJA)
        self.fila.inserir(atendimento)

        self.assertTrue(self.fila.possui_proximo())


class TestProntoSocorroService(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente para os testes do serviço do pronto-socorro."""
        self.pacientes_repo = {}  # Simula um repositório de pacientes
        self.atendimentos_repo = {}  # Simula um repositório de atendimentos
        self.pronto_socorro = ProntoSocorroService(self.pacientes_repo, self.atendimentos_repo)

    def test_inserir_fila_atendimento(self):
        """Testa se um atendimento é corretamente inserido na fila do pronto-socorro."""
        paciente = Paciente("Fernando", "22233344455", "fernando@email.com", "30/07/1992")
        atendimento = Atendimento(paciente, Risco.AMARELO)

        resultado = self.pronto_socorro.inserir_fila_atendimento(atendimento)
        self.assertTrue(resultado)

    def test_chamar_proximo(self):
        """Testa se chamar_proximo() respeita a ordem de prioridade."""
        paciente1 = Paciente("Gabriel", "44455566677", "gabriel@email.com", "12/09/1995")
        paciente2 = Paciente("Helena", "77788899900", "helena@email.com", "25/05/1980")

        atendimento1 = Atendimento(paciente1, Risco.VERDE)
        atendimento2 = Atendimento(paciente2, Risco.VERMELHO)

        self.pronto_socorro.inserir_fila_atendimento(atendimento1)
        self.pronto_socorro.inserir_fila_atendimento(atendimento2)

        self.assertEqual(self.pronto_socorro.chamar_proximo(), atendimento2)
        self.assertEqual(self.pronto_socorro.chamar_proximo(), atendimento1)
