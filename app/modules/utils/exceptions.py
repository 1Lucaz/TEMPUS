from fastapi import HTTPException, status

@staticmethod
def tratar_exception(e: Exception):
    mensagem = str(e)

    if "NÃO ENCONTRADO" in mensagem or "NÃO EXISTE" in mensagem or "NÃO ENCONTRADA":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensagem)

    if "Nenhum dado" in mensagem:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensagem)

    if "JÁ CADASTRADO" in mensagem or "JÁ EM USO" in mensagem:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mensagem)

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mensagem)