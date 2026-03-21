from fastapi import status

class AppException(Exception):

    def __init__(self, mensagem : str, status_code:int, causa: str | None = None):
        self.mensagem = mensagem
        self.status_code = status_code
        self.causa = causa



class BadRequest(AppException):
    def __init__(self, causa: str | None = None):
        super().__init__("Solicitação Inválida. A solicitação não pôde ser compreendida pelo servidor",
                         status.HTTP_400_BAD_REQUEST, causa)

class NotFound(AppException):
    def __init__(self, causa: str | None = None):
        super().__init__("Recurso não encontrado ou inexistente", status.HTTP_404_NOT_FOUND, causa)

class Conflict(AppException):
    def __init__(self, causa: str | None = None):
        super().__init__("Recurso já em uso", status.HTTP_409_CONFLICT, causa)

class InternalServerError (AppException):
    def __init__(self, causa: str | None = None):
        super().__init__("Erro no servidor, infelizmente deu xerém", status.HTTP_500_INTERNAL_SERVER_ERROR, causa)
