class PSBaseError(Exception):
    def __init__(self, message: str):
        self.message = message

class ValidacaoError(PSBaseError):
    def __init__(self, message: str):
        self.message = message

class FilaVaziaError(PSBaseError):
    def __init__(self, message: str):
        self.message = message

class CPFDuplicadoError(PSBaseError):
    def __init__(self, message: str):
        self.message = message

class PacienteNaoCadastradoError(PSBaseError):
    def __init__(self, message: str):
        self.message = message