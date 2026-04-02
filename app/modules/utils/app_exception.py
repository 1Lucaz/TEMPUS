from fastapi import status, HTTPException


class BadRequest(HTTPException):
    def __init__(self, causa: str | None = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Solicitação Inválida. A solicitação não pôde ser compreendida pelo servidor")
        self.causa=causa

class NotFound(HTTPException):
    def __init__(self, causa: str | None = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Recurso não encontrado ou inexistente")
        self.causa = causa

class Conflict(HTTPException):
    def __init__(self, causa: str | None = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="Recurso já em uso")
        self.causa = causa

class InternalServerError (HTTPException):
    def __init__(self, causa: str | None = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no servidor, infelizmente deu xerém")
        self.causa = causa

class Forbidden (HTTPException):
    def __init__(self, causa: str | None = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Operação não autorizada")
        self.causa = causa

class Unauthorized (HTTPException):
    def __init__(self, causa: str | None = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas para esta operação")
        self.causa = causa