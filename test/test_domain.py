import unittest
from datetime import datetime
from main.error import ValidacaoError
from main.domain import Paciente, FilaAtendimento, Risco, Atendimento

#corrigi o nome da class, o test tem que ser primeiro
class TestEntities(unittest.TestCase):
    def test_nome_pessoa_validate(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="   ", cpf="11111111111", email = "teste@teste.com", nascimento="11/11/1111")
        self.assertIn("nome", context.exception.message)