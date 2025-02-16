import unittest
from datetime import datetime
from main.error import ValidacaoError
from main.domain import Paciente, FilaAtendimento, Risco, Atendimento

#corrigi o nome da class, o test tem que ser primeiro
class TestEntities(unittest.TestCase):
    def test_nome_pessoa_validate(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="   ", cpf="11111111111", email = "teste@teste.com", nascimento="11/11/1111")
        self.assertIn("nome", context.exception.args[0])
        
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="12345", cpf="11111111111", email="teste@teste.com", nascimento="11/11/1111")
        self.assertIn("caracteres inválidos", context.exception.args[0])
    
    
    def test_cpf_validate(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="Teste", cpf="abc", email="teste@teste.com", nascimento="11/11/1111")
        self.assertIn("CPF inválido", context.exception.args[0])

        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="Teste", cpf="123", email="teste@teste.com", nascimento="11/11/1111")
        self.assertIn("CPF inválido", context.exception.args[0])


    def test_email_validate(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="Teste", cpf="11111111111", email="email_invalido", nascimento="11/11/1111")
        self.assertIn("E-mail inválido", context.exception.args[0])

        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="Teste", cpf="11111111111", email="teste@com", nascimento="11/11/1111")
        self.assertIn("E-mail inválido", context.exception.args[0])


    def test_nascimento_validate(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="Teste", cpf="11111111111", email="teste@teste.com", nascimento="31/02/2020")
        self.assertIn("Data de nascimento inválida", context.exception.args[0])

        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="Teste", cpf="11111111111", email="teste@teste.com", nascimento="11/11/3000")
        self.assertIn("A data de nascimento não pode ser futura", context.exception.args[0])


    def test_paciente_valido(self):
        paciente = Paciente(nome="Maria Silva", cpf="12345678901", email="maria@example.com", nascimento="15/05/1995")
        self.assertEqual(paciente.nome, "Maria Silva")
        self.assertEqual(paciente.cpf, "12345678901")
        self.assertEqual(paciente.email, "maria@example.com")
        self.assertEqual(paciente.nascimento, "15/05/1995")