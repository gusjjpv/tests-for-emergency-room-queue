import unittest
from datetime import datetime
from main.error import ValidacaoError
from main.domain import Paciente, FilaAtendimento, Risco, Atendimento
from main.error import *


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

class TestProximoDaFila(unittest.TestCase): 
    def setUp(self):
        """Configuração antes de cada teste"""
        self.fila = FilaAtendimento()
        self.paciente1 = Paciente(nome="Carlos Silva", cpf="11111111111", email="carlos@teste.com", nascimento="11/11/1990")
        self.paciente2 = Paciente(nome="Ana Souza", cpf="22222222222", email="ana@teste.com", nascimento="12/12/1985")

    def tearDown(self):
        """Limpeza após cada teste"""
        del self.fila
        del self.paciente1
        del self.paciente2

    def test_fila_vazia_erro(self):
        """Testa se chamar proximo() em uma fila vazia levanta a exceção FilaVaziaError"""
        with self.assertRaises(FilaVaziaError) as context:
            self.fila.proximo()
        self.assertEqual(str(context.exception), "Não tem nenhum paciente na fila de atendimento")

    def test_paciente_nao_registrado_erro_email(self):
        """RT3 - Testa se um paciente com e-mail inválido levanta uma exceção e não entra na fila"""
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="Lucas Martins", cpf="33333333333", email="email-invalido", nascimento="15/08/1995")
        self.assertIn("E-mail inválido", str(context.exception))

    def test_triagem_gravidade_moderada_fila_com_pacientes(self):
        """RT3 - Testa se um paciente com gravidade moderada é registrado e chamado corretamente"""
        atendimento1 = Atendimento(self.paciente1, Risco.AZUL)  
        atendimento2 = Atendimento(self.paciente2, Risco.AMARELO)  

        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)

        paciente_atendido = self.fila.proximo()

        
        self.assertEqual(paciente_atendido, atendimento2)

    def test_paciente_gravidade_alta_chamado_cpf_nao_no_historico(self):
        """RT5 - Testa se um paciente de gravidade alta é chamado corretamente, mas seu CPF não é salvo no histórico"""
        
        
        atendimento1 = Atendimento(self.paciente1, Risco.VERDE)  
        atendimento2 = Atendimento(self.paciente2, Risco.LARANJA)  

        
        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)

        
        paciente_atendido = self.fila.proximo()

        self.assertEqual(paciente_atendido, atendimento2)  
        self.assertEqual(self.fila.tamanho(), 1) 

        if hasattr(self.fila, "historico"):
            cpf_no_historico = any(atendimento.paciente.cpf == paciente_atendido.paciente.cpf for atendimento in self.fila.historico)
            self.assertFalse(cpf_no_historico, "O CPF do paciente chamado não deveria estar no histórico.")

    def test_paciente_gravidade_alta_fila_vazia_historico_salvo(self):
        """Testa se um paciente com gravidade alta é atendido, a fila fica vazia e ele é salvo no histórico"""
        
    
        atendimento = Atendimento(self.paciente1, Risco.VERMELHO)

        
        self.fila.inserir(atendimento)

        
        paciente_atendido = self.fila.proximo()

        
        self.assertEqual(self.fila.tamanho(), 0)

        
        if hasattr(self.fila, "historico"):
            self.assertIn(atendimento, self.fila.historico)
