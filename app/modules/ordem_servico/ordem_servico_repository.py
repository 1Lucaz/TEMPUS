from sqlalchemy.orm import Session
from app.modules.ordem_servico.ordem_servico_model import OrdemServico


class OrdemServicoRepository:

    def __init__(self, db: Session):
        self.db = db


    def salvar_ordem(self, ordem: OrdemServico) -> OrdemServico:
        self.db.add(ordem)
        self.db.flush()
        return ordem
    
    # ////
    
    
    def atualizar_ordem(self, id: int, dados_novos: dict) -> OrdemServico | None:

        if id is None or dados_novos is None:
            return None

        ordem_antiga = self.db.get(OrdemServico, id)

        if ordem_antiga is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(ordem_antiga, campo):
                setattr(ordem_antiga, campo, valor)

        self.db.flush()
        return ordem_antiga


    def busca_dinamica(
        self,
        cliente_id: int | None = None,
        status: str | None = None,
        ativo: bool | None = None
    ) -> list[OrdemServico]:

        query = self.db.query(OrdemServico)

        condicionais = {
            "cliente_id": cliente_id,
            "status": status,
            "ativo": ativo
        }

        for campo, dado in condicionais.items():

            if dado is None:
                continue

            query = query.filter_by(**{campo: dado})

        return query.all()


    def desativar_ordem(self, id: int) -> OrdemServico | None:

        if id is None:
            return None

        ordem = self.db.get(OrdemServico, id)

        if ordem is None:
            return None

        if not ordem.ativo:
            return ordem

        ordem.ativo = False
        self.db.flush()

        return ordem


    def buscar_por_id(self, id: int) -> OrdemServico | None:

        if id is None:
            return None

        ordem = self.db.get(OrdemServico, id)

        if ordem is None:
            return None

        return ordem
    
    
    
    