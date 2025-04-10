# Importações de bibliotecas externas
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS

# Importações internas do projeto
from sqlalchemy.exc import IntegrityError
from model import Session, Plano
from logger import logger
from schemas import *


# Configurações iniciais da API
info = Info(
    title="Minha API",
    version="1.0.0",
    security=[{"bearerAuth": []}]
)

app = OpenAPI(
    __name__,
    info=info,
    security_schemes={
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
)

CORS(app)

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"
jwt = JWTManager(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
plano_tag = Tag(name="Plano", description="Adição, visualização e remoção de planos à base")
Comentario_tag = Tag(name="Comentário", description="Adição de um comentário à planos cadastrados na base")


# Rota: Página Inicial (Documentação)
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger"""
    return redirect('/openapi/swagger')

# Rota: Adição de Plano
@app.post('/plano', tags=[plano_tag], security=[{"bearerAuth": []}],
          responses={"200": PlanoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
@jwt_required()
def add_plano(body: PlanoSchema):
    """Adiciona um novo plano à base de dados; Retorna uma representação
     dos planos e comentários associados."""
    
    usuario_id = get_jwt_identity()
    try:
        form = PlanoSchema(**request.get_json())
    except Exception as e:
        return {"message": f"Erro de validação: {str(e)}"}, 422

    plano = Plano(
        revenue=form.revenue,
        nome=form.nome,
        valor=form.valor,
        usuario_id=usuario_id
    )

    try:
        session = Session()
        session.add(plano)
        session.commit()
        return apresenta_plano(plano), 200
    except IntegrityError:
        return {"mesage": "Plano de mesmo nome já salvo na base."}, 409
    except Exception:
        return {"mesage": "Não foi possível salvar novo item."}, 400


# Rota: Busca de todos os Planos
@app.get('/planos', tags=[plano_tag], security=[{"bearerAuth": []}],
         responses={"200": ListagemPlanosSchema, "404": ErrorSchema})
@jwt_required()
def get_planos():
    """Faz a busca por todos os Planos cadastrados. 
        Retorna uma representação da listagem de produtos."""
    
    usuario_id = get_jwt_identity()
    session = Session()
    planos = session.query(Plano).filter(Plano.usuario_id == usuario_id).all()
    return apresenta_planos(planos), 200

# Rota: Remoção de Plano
@app.delete('/plano/<nome>', tags=[plano_tag], security=[{"bearerAuth": []}],
            responses={"200": PlanoDelSchema, "404": ErrorSchema})
@jwt_required()
def del_plano(path: PlanoPathSchema):
    """Deleta um Plano a partir do nome de plano informado.
        Retorna uma mensagem de confirmação de remoção."""
    
    nome = unquote(unquote(path.nome))
    session = Session()

    count = session.query(Plano).filter(Plano.nome == nome).delete()
    session.commit()

    if count:
        return {'message': "Plano removido", "id": nome}, 200
    else:
        return {'message': "Plano não encontrado na base."}, 404

# Rota: Busca de Plano
@app.get('/plano', tags=[plano_tag], security=[{"bearerAuth": []}],
         responses={"200": ListagemPlanosSchema, "404": ErrorSchema})
@jwt_required()
def busca_plano(body: PlanoBuscaSchema):
    """Faz a busca por produtos em que o termo passando  Produto a partir do id do produto.
        Retorna uma representação dos produtos e comentários associados."""
    
    try:
        data = PlanoBuscaSchema(**request.args)
    except Exception as e:
        return {"message": f"Erro de validação: {str(e)}"}, 422

    nome = unquote(data.nome)
    session = Session()
    planos = session.query(Plano).filter(Plano.nome.ilike(f"%{nome}%")).all()
    return apresenta_planos(planos), 200

# Rota: Alteração de Plano
@app.put('/plano/<nome>', tags=[plano_tag], security=[{"bearerAuth": []}],
         responses={"200": PlanoViewSchema, "404": ErrorSchema, "500": ErrorSchema})
@jwt_required()
def editar_plano(path: PlanoPathSchema, body: PlanoSchema):
    """Atualiza um Plano existente com base no nome informado.
        Retorna os dados atualizados do plano."""
    
    usuario_id = get_jwt_identity()
    nome = unquote(path.nome)

    session = Session()
    plano = session.query(Plano).filter(Plano.nome == nome, Plano.usuario_id == usuario_id).first()

    if not plano:
        return {"message": "Plano não encontrado no banco de dados"}, 404

    if body.revenue is not None:
        plano.revenue = body.revenue
    if body.nome:
        plano.nome = body.nome
    if body.valor is not None:
        plano.valor = body.valor

    try:
        session.commit()
        return apresenta_plano(plano), 200
    except Exception as e:
        session.rollback()
        return {"message": f"Erro ao atualizar plano: {str(e)}"}, 500
    finally:
        session.close()
