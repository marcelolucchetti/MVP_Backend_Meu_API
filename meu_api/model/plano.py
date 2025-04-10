from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from . import Base

class Plano(Base):
    __tablename__ = 'plano'

    id = Column("pk_plano", Integer, primary_key=True)
    revenue = Column(String(140))
    nome = Column(String(140))
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())
    usuario_id = Column(Integer)


    def __init__(self, revenue: str, nome: str, valor: float,
                 usuario_id: int,
                 data_insercao: Union[DateTime, None] = None):
        """Cria um Plano.
        
        Arguments: 
            revenue: Se é gasto ou receita.
            nome: o nome do gasto/receita.
            valor: o valor esperado do gasto/receita.
            usuario_id: ID do usuário dono do plano.
            data_insercao: data de quando o plano foi inserido à base."""
        self.revenue = revenue
        self.nome = nome
        self.valor = valor
        self.usuario_id = usuario_id

        if data_insercao:
            self.data_insercao = data_insercao
