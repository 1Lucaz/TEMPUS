from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import cast

from app.modules.categoria.categoria_model  import CategoriaServico



class CategoriaRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def registrar_Categoria(self, categoria: CategoriaServico):
        self.db.add(categoria)
        self.db.flush()
        return categoria



    
    def buscar_uma_categoria(self,id: int | None = None,
                             descricao: str | None = None ) -> CategoriaServico | None:

        consulta = select(CategoriaServico)

        if id is not None:
            consulta = consulta.where(CategoriaServico.id == id)

        if descricao is not None:
            consulta = consulta.where(CategoriaServico.descricao == descricao)

        return   self.db.execute(consulta).scalar_one_or_none()
    
    
    
    
    def busca_por_id(self,categoria_id):
        consulta = select(CategoriaServico).where(CategoriaServico.id==categoria_id)
        return self.db.execute(consulta).scalar_one_or_none()
    
    def buscar_todos(self):
        consulta = select(CategoriaServico)
        return self.db.execute(consulta).scalars().all()
    
    
    
    def atualizar_categoria(self, id: int, dados_novos: dict):
        categoria = cast(CategoriaServico | None, self.db.get(CategoriaServico, id))
        if not categoria:
            return None
        for campo, valor in dados_novos .items():
            if hasattr(categoria, campo):
                setattr(categoria, campo, valor)
        return categoria
    
    
    def deletar_categoria(self, id: int):
        categoria = self.buscar_por_id(id)
        
        if not categoria:
            return False

        self.db.delete(categoria)
        self.db.commit()
        
        return True
    
    