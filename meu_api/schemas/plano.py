from pydantic import BaseModel
from typing import Optional, List
from model.plano import Plano


class PlanoSchema(BaseModel):
    """Define como um novo plano a ser inserido deve ser representado."""
    revenue: str = "Gasto" 
    nome: str = "Aluguel"
    valor: float = 980

class PlanoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca. Que
    será feita apenas com base no nome do plano."""
    nome: str = "Aluguel"

class ListagemPlanosSchema(BaseModel):
    """Define como uma listagem de planos será retornada."""
    planos: List[PlanoSchema]

def apresenta_planos(planos: List[Plano]):
    """Retorna uma representação do plano seguindo o schema definido em PlanoViewSchema."""
    result = []
    for plano in planos:
        result.append({
            "revenue": plano.revenue,
            "nome": plano.nome,
            "valor": plano.valor,
        })
    
    return {"planos": result}

class PlanoViewSchema(BaseModel):
    """Define como um plano será retornado: plano + comentários."""
    id: int = 1
    revenue: str = "Gasto"
    nome: str = "Aluguel"
    valor: float = 980
    total_comentarios: int = 1

class PlanoDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição de remoção."""
    mesage: str
    nome: str

def apresenta_plano(plano: Plano):
    """Retorna uma representação do plano seguindo o shema definido em PlanoViewSchema."""
    return{
        "id": plano.id,
        "revenue": plano.revenue,
        "nome": plano.nome,
        "valor": plano.valor,
    }

class PlanoAlteraSchema(BaseModel):
    """Define como será alterado uma variável no Plano"""
    nome: str 
    valor: float 

class PlanoPathSchema(BaseModel):
    """Define o path de um plano que será deletado ou editado"""
    nome: str