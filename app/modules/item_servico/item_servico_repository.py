from sqlalchemy.orm import Session
from app.modules.item_servico.item_servico_model import ItemServico


class ItemServicoRepository:

    def __init__(self, db: Session):
        self.db = db
        
        
    def salvar_item(self, item: ItemServico) -> ItemServico:
        self.db.add(item)
        self.db.flush()
        return item
    
    def atualizar_item(self, id: int, dados_novos: dict) -> ItemServico | None:

        if id is None or dados_novos is None:
            return None

        item_antigo = self.db.get(ItemServico, id)

        if item_antigo is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(item_antigo, campo):
                setattr(item_antigo, campo, valor)

        self.db.flush()
        return item_antigo
    
    def busca_dinamica(
        self,
        ordem_servico_id: int | None = None,
        servico_id: int | None = None,
        ativo: bool | None = None
    ) -> list[ItemServico]:

        query = self.db.query(ItemServico)

        condicionais = {
            "ordem_servico_id": ordem_servico_id,
            "servico_id": servico_id,
            "ativo": ativo
        }

        for campo, dado in condicionais.items():
            if dado is None:
                continue

            query = query.filter_by(**{campo: dado})

        return query.all()
    
    def desativar_item(self, id: int) -> ItemServico | None:

        if id is None:
            return None

        item = self.db.get(ItemServico, id)

        if item is None:
            return None

        if not item.ativo:
            return item

        item.ativo = False
        self.db.flush()

        return item
    
    
    def buscar_por_id(self, id: int) -> ItemServico | None:

        if id is None:
            return None

        item = self.db.get(ItemServico, id)

        if item is None:
            return None

        return item
    
    