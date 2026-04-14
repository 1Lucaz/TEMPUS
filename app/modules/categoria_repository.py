from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.categoria_item_servico.categoria_item_servico_model  import CategoriaServico



class CategoriaRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def registrar_Categoria(self, categoria: CategoriaServico):
        self.db.add(categoria)
        self.db.flush()
        return categoria

    def busca_por_id(self,categoria_id):
        consulta = select(CategoriaServico).where(CategoriaServico.id==categoria_id)
        return self.db.execute(consulta).scalar_one_or_none()
    
    def buscar_todos(self):
        consulta = select(CategoriaServico)
        return self.db.execute(consulta).scalars().all()
    