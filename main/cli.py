from main.service import *
from colorama import Fore, Style

class TerminalClient:
    """
    Cliente em linha de comando para o sistema de controle de fila de atendimentos de um pronto-socorro.
    """
    def __init__(self, ps_service: ProntoSocorroService):
        self.ps_service = ps_service

    def mostrar_menu(self):
        print("\n--- MENU ---")
        print("1 - Registrar Paciente")
        print("2 - Registrar Atendimento")
        print("3 - Chamar Próximo da Fila")
        print("4 - Buscar Histórico de Atendimento")
        print("5 - Sair")


    def registrar_paciente(self):
        print("\n--- REGISTRAR PACIENTE ---")
        nome = input("Nome: ")
        cpf = input("CPF (apenas números): ")
        email = input("E-mail: ")
        nascimento = input("Data de nascimento (DD/MM/YYYY): ")

        try:
            paciente = self.ps_service.registrar_paciente(nome, cpf, email, nascimento)
            print(f"\nPaciente registrado com sucesso:\n{paciente}")
        except PSBaseError as e:
            print(Fore.RED + f"\nErro ao registrar paciente: {e.message}" + Style.RESET_ALL)


    def registrar_atendimento(self):
        print("\n--- REGISTRAR ATENDIMENTO ---")
        cpf = input("CPF do paciente (apenas números): ")

        try:
            # Verifica se o paciente está cadastrado
            paciente = self.ps_service.pacientes.buscar(cpf)
            if paciente is None:
                print(Fore.RED + "\nPaciente não encontrado." + Style.RESET_ALL)
                return

            # Perguntas para a triagem
            print("\nResponda as perguntas de triagem (Sim ou Não):")
            risco_morte = input("O paciente corre risco de morte? ").strip().lower() == "sim"
            gravidade_alta = input("O paciente tem gravidade alta? ").strip().lower() == "sim"
            gravidade_moderada = input("O paciente tem gravidade moderada? ").strip().lower() == "sim"
            gravidade_baixa = input("O paciente tem gravidade baixa? ").strip().lower() == "sim"
            ficha = FichaAnalise(risco_morte, gravidade_alta, gravidade_moderada, gravidade_baixa)

            # Classifica o risco
            risco = self.ps_service.classificar_risco(ficha)
            print(f"\nClassificação de risco: {risco.name}")

            # Registra o atendimento e insere na fila
            atendimento = self.ps_service.registrar_atendimento(paciente, risco)
            self.ps_service.inserir_fila_atendimento(atendimento)
            print(f"\nAtendimento registrado e inserido na fila:\n{atendimento}")
        except PSBaseError as e:
            print(Fore.RED + f"\nErro ao registrar atendimento: {e.message}" + Style.RESET_ALL)


    def chamar_proximo(self):
        print("\n--- CHAMAR PRÓXIMO DA FILA ---")
        try:
            proximo = self.ps_service.chamar_proximo()
            print(f"\nPróximo Paciente:\n{proximo}")
        except PSBaseError as e:
            print(Fore.RED + f"\nErro ao chamar próximo: {e.message}" + Style.RESET_ALL)


    def buscar_historico(self):
        print("\n--- BUSCAR HISTÓRICO DE ATENDIMENTO ---")
        cpf = input("CPF do paciente (apenas números): ")

        try:
            # Verifica se o paciente está cadastrado
            paciente = self.ps_service.pacientes.buscar(cpf)
            if paciente is None:
                print(Fore.RED + "\nPaciente não encontrado." + Style.RESET_ALL)
                return

            # Busca o histórico
            historico = self.ps_service.buscar_historico(paciente)
            print(f"\nHistórico de atendimentos para {paciente.nome}:")
            for atendimento in historico:
                print(atendimento)
        except PSBaseError as e:
            print(Fore.RED + f"\nErro ao buscar histórico: {e.message}" + Style.RESET_ALL)

    def executar(self):
        # Inicializa o cliente do serviço do pronto-socorro
        while True:
            self.mostrar_menu()
            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":
                self.registrar_paciente()
            elif opcao == "2":
                self.registrar_atendimento()
            elif opcao == "3":
                self.chamar_proximo()
            elif opcao == "4":
                self.buscar_historico()
            elif opcao == "5":
                print("\nSaindo do sistema...")
                break
            else:
                print(Fore.RED + "\nOpção inválida, tente novamente." + Style.RESET_ALL)
